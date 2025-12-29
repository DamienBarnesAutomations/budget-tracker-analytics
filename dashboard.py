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
df = get_data()
st.markdown("""
    <style>
    /* Reduce padding at the top of the page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    /* Reduce gap between individual elements */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
st.set_page_config(page_title="Travel Expenses", layout="wide")

st.subheader("🌍 Travel Expenses")



if df.empty:
    st.warning("No data found in 'cleaned_data'. Please upload a CSV via the Telegram bot.")
    logger.info("Dashboard displayed with empty state.")
else:
    plot_total_spend(df.copy())
    plot_daily_average_per_category(df.copy())
    plot_cumulative_burn(df.copy())
    chart_daily_avg_category_per_country(df.copy())

# --- 6. RECENT TRANSACTIONS ---
with st.expander("📝 Recent Transactions"):
    st.write("Latest entries ...")
    st.dataframe(df.head(15))