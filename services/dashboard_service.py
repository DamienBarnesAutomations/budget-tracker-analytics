import os
import pandas as pd
import numpy as np
import logging
from services.google_sheet_services import GoogleSheetsService
import streamlit as st
import plotly.express as px

from transformations.data_transformations import (
    calculate_daily_avg_category_per_country,
    calculate_daily_average_per_category,
    calculate_average_daily_budget_per_country,
    calculate_total_spend_per_country,
    calculate_cumulative_spend_per_country_by_day
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
            barmode="overlay",
            text="Daily_Avg",
            labels={"Daily_Avg": "Avg Daily Spend (€)", "Category": "Expense Type"},
            template="plotly_dark"
        )

        # Style the numbers on top of the bars
        fig.update_traces(textposition='outside')
        fig.update_layout(
            uniformtext_minsize=8, 
            uniformtext_mode='hide',
            # Move legend to the top horizontal
            legend=dict(
                orientation="h",   # Horizontal orientation
                yanchor="bottom",
                y=1.02,            # Places it just above the plotting area
                xanchor="center",
                x=0.5              # Centers the legend
            ),
            # Increase top margin slightly so the legend doesn't overlap the title
            margin=dict(t=80) 
        )

        # 1. Lock the Axes (Prevents pinching/zooming)
        fig.update_xaxes(fixedrange=True)
        fig.update_yaxes(fixedrange=True)

        # 2. Disable Dragging (Prevents selecting/panning)
        fig.update_layout(dragmode=False)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add some expenses with Country and Category tags to see the chart!")

def chart_daily_avg_category_per_country2(df):
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
    # Prepare data
    burn_df = df.groupby('Date')['Amount'].sum().reset_index().sort_values('Date')
    burn_df['Cumulative_Total'] = burn_df['Amount'].cumsum()

    st.caption("📈 Total Spending Over Time")
    
    # Use area chart for a "cleaner" look
    fig = px.area(
        burn_df,
        x='Date',
        y='Cumulative_Total',
        template="plotly_dark",
        color_discrete_sequence=['#00CC96'] # A nice "Safe" green
    )

    # 1. Add Budget Ceiling
    fig.add_hline(y=TOTAL_BUDGET, line_dash="dash", line_color="#FF4B4B", line_width=1)

    # 2. Compress and Clean (The "Neat" settings)
    fig.update_layout(
        height=250,                    # Reduced height
        margin=dict(l=0, r=0, t=10, b=0), # Zero out margins to use full width
        xaxis_title="",                # Remove redundant titles
        yaxis_title="",
        showlegend=False,
        hovermode="x unified",         # Cleanest hover experience for mobile
        # Remove gridlines for that "Minimalist" look
        xaxis=dict(showgrid=False, fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor="#333", fixedrange=True),
        dragmode=False
    )

    # 3. Smooth the line (Optional: makes it look less jagged)
    fig.update_traces(line_shape='spline', line_width=2)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    

def plot_total_spend(df):
    total_spent = df['Amount'].sum()
    total_days = df['Date'].nunique()
    daily_avg = total_spent / total_days if total_days > 0 else 0
    remaining = TOTAL_BUDGET - total_spent

    # 2. Display side-by-side
    col1, col2 = st.columns([1, 1], gap="small")

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
    st.caption("Daily Budget Allocation")

    fig_pie = px.pie(
        cat_avg_df, 
        values='Daily_Avg_Euro', 
        names='Category',
        hole=0.5,
        template="plotly_dark"
    )

    # 1. Put Category Names and Percentages directly on the chart
    fig_pie.update_traces(
        textinfo='label+percent', # Shows 'Food 25%' on the slice
        textposition='outside',   # Keeps labels outside so they don't overlap in the 'hole'
        insidetextorientation='radial'
    )

    # 2. Kill the legend and adjust height
    fig_pie.update_layout(
        height=450,               # Slightly taller to accommodate outside labels
        showlegend=False,         # Hiding the messy scrolling legend
        margin=dict(l=50, r=50, t=20, b=20), # Add side margins so labels don't clip
    )

    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    
def plot_total_and_average_per_country(df):
    column1, column2 = st.columns(2)
    total_spend = calculate_total_spend_per_country(df.copy())
    bar_data = calculate_average_daily_budget_per_country(df.copy())

    with column1:
        st.caption("🏳️‍🌈 By Country (Total)")
        total_spend = total_spend[total_spend['Amount'] > 0]
        max_val = total_spend['Amount'].max()
        fig_country_total = px.bar(
            total_spend,
            x='Amount',
            y='Country',
            orientation='h',
            text='Amount',
            template="plotly_dark",
            color='Country',
            log_x=True
        )

        # 3. Apply Mobile-Friendly Styling & Scroll-Lock
        fig_country_total.update_traces(
            texttemplate='€%{text:,.2f}', 
            textposition='inside',
            insidetextanchor='end'
        )
        
        fig_country_total.update_layout(
            height=300, # Compact height
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_fixedrange=True, # Disable Zoom
            yaxis_fixedrange=True, # Disable Zoom
            dragmode=False,        # Disable Pan
            coloraxis_showscale=False,
            xaxis_title="Total Euros (€)",
            yaxis_title="",
            xaxis_type="log",
            showlegend=False,
            xaxis_range=[0, np.log10(max_val * 1.2)], # Starts the 'visual' bar at €1
        )

        # 4. Display without the floating menu bar
        st.plotly_chart(fig_country_total, width='stretch', config={'displayModeBar': False})


    with column2:
        # B. Daily Average by Country (Bar)
        st.caption("🏳️‍🌈 By Country (Daily)")
        fig_bar = px.bar(bar_data, x='Avg_Daily_Budget', y='Country', orientation='h', text_auto='.2f', template="plotly_dark", color='Country')
        fig_bar.update_layout(
            height=300, # Compact height
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False,
            xaxis_fixedrange=True, # Disable Zoom
            yaxis_fixedrange=True, # Disable Zoom
            dragmode=False,        # Disable Pan,
            coloraxis_showscale=False, xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_bar, width='stretch', config={'displayModeBar': False})

def plot_country_comparison_burn(df):
    chart_data = calculate_cumulative_spend_per_country_by_day(df)
    
    if chart_data.empty:
        st.info("No data available for comparison.")
        return

    st.caption("📈 Cumulative Spend Comparison (Day-by-Day)")

    fig = px.line(
        chart_data,
        x='Day_Num',
        y='Cumulative_Total',
        color='Country',
        template="plotly_dark",
        labels={
            'Day_Num': 'Day in Country',
            'Cumulative_Total': 'Total Spent (€)'
        }
    )

    # Apply "Neat & Compressed" Styling
    fig.update_layout(
        height=350, # Increased slightly to accommodate the legend
        margin=dict(l=10, r=10, t=10, b=80), # Increased bottom margin for legend space
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        dragmode=False,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,            # Pulls it further down away from the X-axis
            xanchor="center",
            x=0.5,
            entrywidth=70,     # Forces items to have specific widths to prevent overlap
            entrywidthmode="pixels",
            title=""
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#333")
    )
    # Make the lines slightly thicker for mobile visibility
    fig.update_traces(line=dict(width=3))

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



    
