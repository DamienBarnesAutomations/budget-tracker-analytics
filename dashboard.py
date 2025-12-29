import streamlit as st
import plotly.express as px
import os
import pandas as pd
import logging
from services.dashboard_service import (
    get_data, chart_daily_avg_category_per_country, plot_cumulative_burn, plot_total_spend,
    plot_daily_average_per_category, plot_total_and_average_per_country, plot_country_comparison_burn
)

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- UI LAYOUT ---
df = get_data()
st.set_page_config(
    page_title="Travel Expenses",
    page_icon="🌍",
    layout="centered", # Better for mobile-first scrolling
    initial_sidebar_state="collapsed" # Keeps the menu out of the way on small screens
)

st.header("🌍 Travel Expenses")

if df.empty:
    st.warning("No data found in 'cleaned_data'. Please upload a CSV via the Telegram bot.")
    logger.info("Dashboard displayed with empty state.")
else:
    plot_total_spend(df.copy())
    plot_daily_average_per_category(df.copy())
    plot_total_and_average_per_country(df.copy())
    burn1, burn2 = st.columns([1, 1], gap="small")
    with burn1:
        plot_cumulative_burn(df.copy())
    with burn2:
        plot_country_comparison_burn(df.copy())
    chart_daily_avg_category_per_country(df.copy())

# --- 6. RECENT TRANSACTIONS ---
with st.expander("📝 Recent Transactions"):
    st.write("Latest entries ...")
    st.dataframe(df.head(15))