import gspread
import logging
import pandas as pd
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

# API permissions required
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class GoogleSheetsService:
    def __init__(self, json_key_path, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        # Authenticate once when the service is initialized
        creds = Credentials.from_service_account_file(json_key_path, scopes=SCOPES)
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
    
