import gspread
import logging
import pandas as pd
import os
import json
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

# API permissions required
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class GoogleSheetsService:
    def __init__(self, json_key_path, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        
        creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        if creds_json:
            # Production: credentials injected as environment variable
            try:
                creds_dict = json.loads(creds_json)
                creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
                logger.info("Loaded credentials from environment variable.")
            except Exception as e:
                logger.error(f"Failed to load credentials from environment variable: {e}")
                raise e
        else:
            # Local development: credentials loaded from file
            if not os.path.exists(json_key_path):
                logger.error(f"Credentials file not found at: {json_key_path}")
                raise FileNotFoundError(f"Credentials file not found at: {json_key_path}")
            creds = Credentials.from_service_account_file(json_key_path, scopes=SCOPES)
            logger.info(f"Loaded credentials from file: {json_key_path}")
            
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(spreadsheet_id)

    def write_dataframe_to_sheet(self, df, sheet_name):
        """Writes a specific Pandas DataFrame to a named sheet tab."""
        try:
            # 1. Prepare data (Headers + Values)
            data = [df.columns.values.tolist()] + df.fillna('').values.tolist()
            
            # 2. Find or create the worksheet
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
                logger.info(f"Created new worksheet: {sheet_name}")

            # 3. Overwrite data
            worksheet.clear()
            worksheet.update('A1', data)
            logger.info(f"Successfully updated {sheet_name} with {len(df)} rows.")
            return True
        except Exception as e:
            logger.error(f"Error writing to sheet {sheet_name}: {e}")
            return False
    
    def read_sheet_to_dataframe(self, sheet_name):
        """Reads a specific sheet tab and returns it as a Pandas DataFrame."""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            logger.info(f"Successfully read {len(df)} rows from {sheet_name}.")
            return df
        except Exception as e:
            logger.error(f"Error reading from sheet {sheet_name}: {e}")
            return pd.DataFrame()
    
