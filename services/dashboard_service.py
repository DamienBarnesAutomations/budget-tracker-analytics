import os
import pandas as pd
import numpy as np
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

TOTAL_BUDGET = 20000 

# Initialize Service
service = None
try:
    if SPREADSHEET_ID:
        service = GoogleSheetsService(JSON_KEY_PATH, SPREADSHEET_ID)
        logger.info("GoogleSheetsService initialized successfully.")
    else:
        logger.warning("GOOGLE_SHEET_ID not set. service will be None.")
except Exception as e:
    logger.error(f"Failed to initialize GoogleSheetsService: {e}")

def get_data():
    if not service:
        logger.error("GoogleSheetsService not initialized.")
        return pd.DataFrame()
    
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



    
