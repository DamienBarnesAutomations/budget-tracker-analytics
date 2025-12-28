import pandas as pd
import logging
import os
from datetime import date, timedelta

# Set up logger for this specific module
logger = logging.getLogger(__name__)

# Import the transformation logic
from transformations.data_transformations import (
    process_main_data, 
)

def load_csv_file(filepath):
    """Reads the CSV from disk with error handling."""
    if not os.path.exists(filepath):
        logger.error(f"❌ File not found: {filepath}")
        return None

    try:
        df = pd.read_csv(filepath)
        logger.info(f"✅ Successfully read CSV with {len(df)} raw rows.")
        return df
    except Exception as e:
        logger.error(f"❌ Failed to parse CSV: {str(e)}")
        return None

def load_and_process_data(filepath):
    """
    Public entry point: Coordinates the loading, transforming, and packaging of data.
    Returns: A dictionary of DataFrames/Series ready for Google Sheets, or None.
    """
    logger.info(f"🚀 Starting orchestration for: {filepath}")
    
    # 1. Load the raw data from disk
    df_raw = load_csv_file(filepath)
    if df_raw is None:
        return None

    try:
        # 2. Initial Clean (The "Master" DataFrame)
        df_main = process_main_data(df_raw)
        
        if df_main is None or df_main.empty:
            logger.error("❌ process_main_data returned empty. Aborting transformations.")
            return None

        # 3. Generate secondary views/transformations
        # We wrap this in a dictionary where keys are intended Sheet Names
        logger.info("Calculating secondary transformations...")
        sheet_data = {
            "Cleaned_Data": df_main.copy(),
    }

        # 4. Final Formatting: Convert Date objects to strings for Google Sheets JSON
        # We do this LAST so the calculation functions above could still use datetime math
        if "Cleaned_Data" in sheet_data:
            sheet_data["Cleaned_Data"]['Date'] = sheet_data["Cleaned_Data"]['Date'].dt.strftime('%Y-%m-%d')

        logger.info("✅ Orchestration complete. Data ready for Google Sheets.")
        return sheet_data

    except Exception as e:
        logger.error(f"❌ Critical error during data orchestration: {str(e)}", exc_info=True)
        return None