import streamlit as st
import plotly.express as px
import os
import pandas as pd
import logging
from services.dashboard_service import (
    get_data, chart_daily_avg_category_per_country, plot_cumulative_burn, plot_total_spend,
    plot_daily_average_per_category
)

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- UI LAYOUT ---
st.title("🌍 Trip Expenses")
df = get_data()



if df.empty:
    st.warning("No data found in 'cleaned_data'. Please upload a CSV via the Telegram bot.")
    logger.info("Dashboard displayed with empty state.")
else:
    plot_total_spend(df.copy())
    plot_daily_average_per_category(df.copy())
    plot_cumulative_burn(df.copy())
    chart_daily_avg_category_per_country(df.copy())