import pandas as pd
import logging
import os
from datetime import date, timedelta

# --- CONSTANTS ---
DATE_COL = 'datePaid'
AMOUNT_COL = 'amountInHomeCurrency'
CATEGORY_COL = 'category'
COUNTRY_COL = 'country' # Added this to match your functions
EXCLUDE_CATEGORY = 'Flights'

logger = logging.getLogger(__name__)

def get_yesterday():
    """Calculates yesterday's date object for filtering."""
    return date.today() - timedelta(days=1)

def process_main_data(df):
    """Performs cleaning, type conversion, and filtering logic."""
    max_date = get_yesterday()
    try:
        # 1. Validation: Ensure required columns exist
        required = [DATE_COL, AMOUNT_COL, CATEGORY_COL]
        if not all(col in df.columns for col in required):
            logger.error(f"❌ Missing columns. Required: {required}")
            return None

        # 2. Select and Rename core columns
        cols_to_keep = [DATE_COL, AMOUNT_COL, CATEGORY_COL]
        new_names = ['Date', 'Amount', 'Category']
        
        if COUNTRY_COL in df.columns:
            cols_to_keep.append(COUNTRY_COL)
            new_names.append('Country')

        df = df[cols_to_keep].copy()
        df.columns = new_names
        
        # 3. Date Cleaning
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True) 

        # 4. NEW: Add Month column for Looker Studio
        # Format: '2025-01' (Better for sorting than 'January')
        df['Month'] = df['Date'].dt.strftime('%Y-%m')

        # 5. Amount Cleaning
        df['Amount'] = df['Amount'].astype(str).str.replace(r'[^\d\.]', '', regex=True)
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df.dropna(subset=['Amount'], inplace=True) 
        df['Amount'] = df['Amount'].abs()

        # 6. Filter Category & Max Date
        df['Category'] = df['Category'].astype(str).str.strip().str.title()
        if 'Country' in df.columns:
            df['Country'] = df['Country'].astype(str).str.strip().str.title()
            
        initial_count = len(df)
        df = df[~df['Category'].isin(["Flights"])]
        df = df[df['Date'].dt.date <= max_date]
        
        logger.info(f"📊 Processed {len(df)} rows. 'Month' column added for Looker Studio.")
        
        return df

    except Exception as e:
        logger.error(f"❌ Error in process_main_data: {str(e)}", exc_info=True)
        return None

def calculate_daily_average_per_category(df):
    """Calculates summary stats and average daily spend per category."""
    if df.empty or 'Date' not in df.columns: 
        return pd.DataFrame()

    # Ensure Date is datetime
    temp_date = pd.to_datetime(df['Date'], errors='coerce')
    
    # Drop rows where date is NaT (invalid)
    valid_dates = temp_date.dropna()
    
    if valid_dates.empty:
        return pd.DataFrame()

    start_date = valid_dates.min()
    end_date = valid_dates.max()
    
    # Calculate duration (using Timestamps directly is safer)
    trip_duration = (end_date - start_date).days + 1

    # Ensure trip_duration is at least 1 to avoid division by zero
    trip_duration = max(trip_duration, 1)

    total_per_cat = df.groupby('Category')['Amount'].sum()
    daily_avg = (total_per_cat / trip_duration).round(2).reset_index()
    daily_avg.columns = ['Category', 'Daily_Avg_Euro']
    logger.info(f"📈 Calculated daily averages over {trip_duration} days.")

    return daily_avg
    

def calculate_weekly_expenditure(df):
    """Calculates total weekly expenditure for bar charts."""
    if df.empty: return pd.Series()

    # Resample by Week starting Monday ('W-MON')
    df_copy = df.copy()
    df_copy.set_index('Date', inplace=True)
    weekly_sum = df_copy['Amount'].resample('W-MON').sum().reset_index()
    
    weekly_sum.columns = ['Week_Start_Date', 'Total_Spend']
    weekly_sum['Week_Start_Date'] = weekly_sum['Week_Start_Date'].dt.strftime('%Y-%m-%d')
    
    return weekly_sum

def calculate_average_daily_budget_per_country(df):
    """Calculates Avg Daily Budget (Total Spend / Distinct Days) per country."""
    if 'Country' not in df.columns or df.empty:
        return pd.DataFrame()

    # 1. Create a copy to avoid SettingWithCopy warnings
    temp_df = df.copy()
    exclude_title = "Ireland".strip().title()
        
    temp_df = temp_df[temp_df['Country'] != exclude_title]

    exclude_Flights_title = "Flights".strip().title()
        
    temp_df = temp_df[temp_df['Category'] != exclude_Flights_title]

    # 2. Force Date column to datetime objects safely
    temp_df['Date'] = pd.to_datetime(temp_df['Date'], errors='coerce')
    
    # 3. Drop rows with invalid dates so they don't mess up the count
    temp_df = temp_df.dropna(subset=['Date'])

    # 4. Total Spend per country
    spend = temp_df.groupby('Country')['Amount'].sum().reset_index()

    # 5. Distinct Days per country (No .dt needed if we do it this way)
    # We convert to just the date part to ignore hours/minutes
    days = temp_df.groupby('Country')['Date'].apply(lambda x: x.dt.date.nunique()).reset_index()
    
    # --- IF THE ABOVE STILL FAILS, USE THIS ALTERNATIVE FOR LINE 5: ---
    # days = temp_df.groupby('Country')['Date'].nunique().reset_index()

    budget_df = pd.merge(spend, days, on='Country')
    budget_df.columns = ['Country', 'Total_Spend', 'Total_Days']
    
    
    # 6. Calculate Average (handle division by zero just in case)
    budget_df['Avg_Daily_Budget'] = (
        budget_df['Total_Spend'] / budget_df['Total_Days'].replace(0, 1)
    ).round(2)
    
    return budget_df.sort_values(by='Avg_Daily_Budget', ascending=True)

def calculate_comparative_weekly_spending(df):
    """Calculates spending by relative week number (Week 1, 2, 3...)"""
    if 'Country' not in df.columns:
        return pd.DataFrame()

    # Create a relative week number per country
    df = df.copy()
    df['Min_Date'] = df.groupby('Country')['Date'].transform('min')
    df['Week_Num'] = ((df['Date'] - df['Min_Date']).dt.days // 7) + 1
    
    weekly_comp = df.groupby(['Country', 'Week_Num'])['Amount'].sum().reset_index()
    
    # Pivot so each Country is a column (Looker Studio loves this for comparisons)
    pivot_df = weekly_comp.pivot(index='Week_Num', columns='Country', values='Amount').fillna(0)
    
    # AGAIN: reset_index() so 'Week_Num' is a column for Looker
    return pivot_df.reset_index()

def calculate_category_percentages(df):
    """Calculates what % of total spend each category represents."""
    if df.empty: return pd.DataFrame()
    
    total_spend = df['Amount'].sum()
    cat_totals = df.groupby('Category')['Amount'].sum().reset_index()
    cat_totals['Percentage'] = (cat_totals['Amount'] / total_spend).round(4)
    return cat_totals.sort_values(by='Percentage', ascending=False)

def calculate_cumulative_spend(df):
    """Calculates a running total of spend over time."""
    if df.empty: return pd.DataFrame()
    
    # Group by date first to handle multiple transactions on the same day
    daily_total = df.groupby('Date')['Amount'].sum().reset_index()
    daily_total = daily_total.sort_values(by='Date')
    daily_total['Cumulative_Total'] = daily_total['Amount'].cumsum().round(2)
    
    # Format date for sheets
    daily_total['Date'] = daily_total['Date'].dt.strftime('%Y-%m-%d')
    return daily_total

def calculate_weekend_vs_weekday(df):
    """Compares average spend on weekends vs weekdays."""
    if df.empty: return pd.DataFrame()
    
    df_temp = df.copy()
    # 5 and 6 are Saturday and Sunday
    df_temp['Is_Weekend'] = df_temp['Date'].dt.dayofweek >= 5
    summary = df_temp.groupby('Is_Weekend')['Amount'].mean().round(2).reset_index()
    summary['Type'] = summary['Is_Weekend'].map({True: 'Weekend', False: 'Weekday'})
    return summary[['Type', 'Amount']]

def calculate_daily_avg_category_per_country(df):
    """Calculates avg spend per category, segmented by country."""
    if 'Country' not in df.columns or df.empty:
        return pd.DataFrame()

    # 1. Get total days spent in each country
    days_per_country = df.groupby('Country')['Date'].nunique().reset_index()
    days_per_country.rename(columns={'Date': 'Days_in_Country'}, inplace=True)

    # 2. Get total spend per category per country
    cat_country_spend = df.groupby(['Country', 'Category'])['Amount'].sum().reset_index()

    # 3. Merge them
    merged = pd.merge(cat_country_spend, days_per_country, on='Country')

    # --- THE FIX ---
    # Ensure columns are numeric before dividing
    merged['Amount'] = pd.to_numeric(merged['Amount'], errors='coerce').fillna(0)
    merged['Days_in_Country'] = pd.to_numeric(merged['Days_in_Country'], errors='coerce').fillna(1)

    # 4. Calculate the average safely
    merged['Daily_Avg'] = (merged['Amount'] / merged['Days_in_Country']).round(2)
    exclude_title = EXCLUDE_CATEGORY.strip().title()
        
    merged = merged[merged['Category'] != exclude_title]
    merged = merged[~merged['Category'].isin(["Medical", "Health", "Shopping"])]
    # 5. Sort
    return merged.sort_values(['Country', 'Daily_Avg'], ascending=[True, False])

def calculate_total_spend_per_country(df):
    """Calculates the absolute total spent in each country."""
    if 'Country' not in df.columns or df.empty:
        return pd.DataFrame()

    total_spend = df.groupby('Country')['Amount'].sum().reset_index()
    # Sort so the highest spending country is at the top
    return total_spend.sort_values(by='Amount', ascending=True)

def calculate_cumulative_spend_per_country_by_day(df):
    """Groups spend by country and day number for comparison."""
    if df.empty:
        return pd.DataFrame()

    # 1. Group by Country and Date to get daily totals
    daily_country = df.groupby(['Country', 'Date'])['Amount'].sum().reset_index()
    daily_country = daily_country.sort_values(['Country', 'Date'])

    # 2. Create the 'Day Number' column (Day 1, 2, 3...) for each country
    daily_country['Day_Num'] = daily_country.groupby('Country').cumcount() + 1

    # 3. Calculate the running total for each country
    daily_country['Cumulative_Total'] = daily_country.groupby('Country')['Amount'].cumsum()

    return daily_country