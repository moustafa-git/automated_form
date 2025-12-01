"""
Google Sheets handler for Vercel deployment.
Since Vercel's filesystem is read-only, we use Google Sheets API instead of Excel.
"""
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SHEET_NAME = os.getenv("SHEET_NAME", "SHOC")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")  # Set this in Vercel environment variables

def get_sheets_client():
    """Initialize Google Sheets client using service account credentials."""
    # Credentials are stored as JSON string in environment variable
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        raise ValueError("GOOGLE_CREDENTIALS_JSON environment variable not set")
    
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)

def append_to_sheets(form_data: dict):
    """
    Append one observation as a new row in Google Sheets.
    Matches the Excel structure: Row 3 = headers, Row 4+ = data.
    """
    if not SPREADSHEET_ID:
        raise ValueError("GOOGLE_SHEET_ID environment variable not set")
    
    client = get_sheets_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    
    try:
        worksheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Sheet '{SHEET_NAME}' not found in spreadsheet")
    
    # Get all values to find next row
    all_values = worksheet.get_all_values()
    
    # Find next row (skip title row, blank row, header row = rows 0, 1, 2)
    if len(all_values) <= 3:
        next_row = 4
        serial_number = 1
    else:
        next_row = len(all_values) + 1
        # Get previous S/N from column A (row index - 1, column 0)
        prev_sn = all_values[-1][0] if len(all_values[-1]) > 0 else None
        try:
            serial_number = int(prev_sn) + 1 if prev_sn else next_row - 3
        except (ValueError, TypeError):
            serial_number = max(1, next_row - 3)
    
    # Prepare row data matching Excel columns (A through R)
    row_data = [
        serial_number,  # A: S/N
        form_data.get("date_occurred", ""),  # B: Date
        form_data.get("observer", ""),  # C: Observer
        form_data.get("company", ""),  # D: Company
        form_data.get("trade_position", ""),  # E: Trade/Position
        form_data.get("observation_group", ""),  # F: Observation Group
        form_data.get("location_area", ""),  # G: Location/Area
        form_data.get("observation_type", ""),  # H: Observation Type
        form_data.get("observation", ""),  # I: Observation
        form_data.get("action", ""),  # J: Action
        form_data.get("action_taken", ""),  # K: Action Taken
        form_data.get("corrective_preventive_action", ""),  # L: Corrective Action / Preventive Action
        form_data.get("priority", ""),  # M: Priority
        form_data.get("risk_rating", ""),  # N: Risk Rating
        form_data.get("custodian", ""),  # O: Custodian
        form_data.get("due_date", ""),  # P: Due Date
        form_data.get("status", ""),  # Q: Status
        form_data.get("comment", ""),  # R: Comment
    ]
    
    # Append the row
    worksheet.append_row(row_data)

