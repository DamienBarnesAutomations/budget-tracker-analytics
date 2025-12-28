import streamlit as st
import plotly.express as px
import os
import pandas as pd
import logging
from services.google_sheet_services import GoogleSheetsService

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
JSON_KEY_PATH = "service_account.json"

# Initialize Service
try:
    service = GoogleSheetsService(JSON_KEY_PATH, SPREADSHEET_ID)
    logger.info("GoogleSheetsService initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize GoogleSheetsService: {e}")
    st.error("Configuration Error: Check your service account key and Sheet ID.")

@st.cache_data(ttl=600)
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

# --- UI LAYOUT ---
st.title("🌍 Trip Expenses")

df = get_data()

if df.empty:
    st.warning("No data found in 'cleaned_data'. Please upload a CSV via the Telegram bot.")
    logger.info("Dashboard displayed with empty state.")
else:
    # Basic Data Cleaning for Analytics
    try:
        # Ensure correct types for calculations
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        st.write(f"Showing {len(df)} transactions.")
        
        # --- THE MAGIC CALCULATION ---
        # 1. Count unique days per country
        days_per_country = df.groupby('Country')['Date'].nunique().to_dict()
        
        # 2. Sum amount by Country AND Category
        summary = df.groupby(['Country', 'Category'])['Amount'].sum().reset_index()
        
        # 3. Apply the Daily Average
        summary['Daily_Avg'] = summary.apply(
            lambda row: row['Amount'] / days_per_country.get(row['Country'], 1), 
            axis=1
        )
        
        # --- THE CHART ---
        fig = px.bar(
            summary, 
            x="Category", 
            y="Daily_Avg", 
            color="Country", 
            barmode="group",
            title="Daily Average Spending per Category",
            labels={"Daily_Avg": "Avg Spend (€)", "Category": "Category"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Optional: Show raw data table below
        with st.expander("View Raw Data"):
            st.dataframe(df)

        logger.info("Dashboard charts rendered successfully.")

    except Exception as e:
        st.error("Error processing data for charts.")
        logger.error(f"Data Processing Error: {e}")