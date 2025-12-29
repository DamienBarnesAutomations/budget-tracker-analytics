import os
import pandas as pd
import logging
from services.google_sheet_services import GoogleSheetsService
import streamlit as st
import plotly.express as px

from transformations.data_transformations import (
    calculate_daily_avg_category_per_country,
    calculate_daily_average_per_category,
    calculate_average_daily_budget_per_country
)

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
JSON_KEY_PATH = "service_account.json"

TOTAL_BUDGET = 20000 


# Initialize Service
try:
    service = GoogleSheetsService(JSON_KEY_PATH, SPREADSHEET_ID)
    logger.info("GoogleSheetsService initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize GoogleSheetsService: {e}")
    st.error("Configuration Error: Check your service account key and Sheet ID.")

#@st.cache_data(ttl=600)
def get_data():
    logger.info("Attempting to fetch data from Google Sheets...")
    try:
        df = service.read_sheet_to_dataframe("Cleaned_Data")
        if df.empty:
            logger.warning("Dataframe returned is empty.")
        else:
            logger.info(f"Successfully loaded {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        return pd.DataFrame()

def chart_daily_avg_category_per_country(df):
    chart_data = calculate_daily_avg_category_per_country(df)
    if not chart_data.empty:
        st.caption("Daily Average Spending per Category")
        
        # Create the Grouped Bar Chart
        fig = px.bar(
            chart_data,
            x="Category",
            y="Daily_Avg",
            color="Country",
            barmode="group", # This puts the bars side-by-side
            text="Daily_Avg", # Shows the number on top of the bar
            title="How much am I spending per day in each country?",
            labels={"Daily_Avg": "Avg Daily Spend (€)", "Category": "Expense Type"},
            template="plotly_dark"
        )

        # Style the numbers on top of the bars
        fig.update_traces(textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        # 1. Lock the Axes (Prevents pinching/zooming)
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)

# 2. Disable Dragging (Prevents selecting/panning)
        fig.update_layout(dragmode=False)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Add some expenses with Country and Category tags to see the chart!")

def plot_cumulative_burn(df):
    # Prepare data: Sort by date and calculate running total
    burn_df = df.groupby('Date')['Amount'].sum().reset_index().sort_values('Date')
    burn_df['Cumulative_Total'] = burn_df['Amount'].cumsum()

    st.caption("📈 Total Spending Over Time")
    fig = px.line(
        burn_df,
        x='Date',
        y='Cumulative_Total',
        #title="📈 Total Spending Over Time (The Burn)",
        labels={'Cumulative_Total': 'Total Euro (€)'},
        template="plotly_dark"
    )
    # Add a "Budget Ceiling" dashed line
    fig.add_hline(y=TOTAL_BUDGET, line_dash="dash", line_color="red", annotation_text="Budget Limit")
    # 1. Lock the Axes (Prevents pinching/zooming)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)

    # 2. Disable Dragging (Prevents selecting/panning)
    fig.update_layout(dragmode=False)
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    

def plot_total_spend(df):
    total_spent = df['Amount'].sum()
    total_days = df['Date'].nunique()
    daily_avg = total_spent / total_days if total_days > 0 else 0
    remaining = TOTAL_BUDGET - total_spent

    # 2. Display side-by-side
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Total Spent", 
            value=f"€{total_spent:,.2f}",
            delta=f"€{remaining:,.2f} remaining",
        )

    with col2:
        st.metric(
            label="Daily Average", 
            value=f"€{daily_avg:,.2f}",
            delta=f"{total_days} days tracked",
            delta_color="normal"
        )

    percent_used = min(total_spent / TOTAL_BUDGET, 1.0)
    days_remaining = (TOTAL_BUDGET - total_spent) / daily_avg

    st.info(f"💡 At €{daily_avg:,.2f}/day, your budget lasts for **{int(days_remaining)} more days**.")
    st.progress(percent_used, text=f"{percent_used:.1%} of budget exhausted")

def plot_daily_average_per_category(df):
    cat_avg_df = calculate_daily_average_per_category(df.copy())

    column1, column2 = st.columns(2)
    with column1:
        st.caption("Daily Budget Allocation")
        # 2. Create Layout
        fig_pie = px.pie(
            cat_avg_df, 
            values='Daily_Avg_Euro', 
            names='Category',
            hole=0.5,
            template="plotly_dark"
        )
    
        fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, width='stretch', config={'displayModeBar': False})
    
    with column2:
        # B. Daily Average by Country (Bar)
        st.caption("🏳️‍🌈 By Country (Daily)")
        bar_data = calculate_average_daily_budget_per_country(df)
        fig_bar = px.bar(bar_data, x='Avg_Daily_Budget', y='Country', orientation='h', text_auto='.2f', template="plotly_dark", color='Avg_Daily_Budget', color_continuous_scale='Reds')
        fig_bar.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="")
        # 1. Lock the Axes (Prevents pinching/zooming)
        fig_bar.update_xaxes(fixedrange=True)
        fig_bar.update_yaxes(fixedrange=True)

        # 2. Disable Dragging (Prevents selecting/panning)
        fig_bar.update_layout(dragmode=False)
        st.plotly_chart(fig_bar, width='stretch', config={'displayModeBar': False})



    
