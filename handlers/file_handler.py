import os
import logging
from processors.file_processor import load_and_process_data
from services.google_sheet_services import GoogleSheetsService

logger = logging.getLogger(__name__)

# Constants from Environment
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
JSON_KEY_PATH = "service_account.json"

def orchestrate_file_process(filepath):
    """
    Orchestrates the full pipeline:
    1. Processing raw CSV into multiple DataFrames.
    2. Uploading each resulting DataFrame to its own tab in Google Sheets.
    """
    # 1. Generate the dictionary of DataFrames
    sheets_data = load_and_process_data(filepath)
    
    if not sheets_data:
        logger.error("❌ Orchestration aborted: No data returned from processor.")
        return False

    # 2. Initialize the Google Sheets Service
    try:
        if not SPREADSHEET_ID:
            logger.error("❌ GOOGLE_SHEET_ID is missing in .env")
            return False

        gs_service = GoogleSheetsService(JSON_KEY_PATH, SPREADSHEET_ID)
        
        # 3. Iterate through the dictionary and write each sheet
        logger.info(f"📤 Uploading {len(sheets_data)} tabs to Google Sheets...")
        
        for sheet_name, df in sheets_data.items():
            success = gs_service.write_dataframe_to_sheet(df, sheet_name)
            if not success:
                logger.warning(f"⚠️ Failed to update sheet: {sheet_name}")

        logger.info("✅ All sheets updated successfully.")
        return True

    except Exception as e:
        logger.error(f"❌ Critical error in file_handler: {str(e)}", exc_info=True)
        return False