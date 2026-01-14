import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config


def authenticate_sheets():
    
    creds = None
    
    # Check if we've logged in before
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If we don't have valid credentials, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next time
        with open(config.TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    # Build and return the Sheets service
    service = build('sheets', 'v4', credentials=creds)
    return service


def setup_sheet_headers(service):
 
    try:
        # Check if the sheet already has data
        result = service.spreadsheets().values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"'{config.SHEET_NAME}'!A1:D1"  # Use single quotes around sheet name for spaces
        ).execute()
        
        values = result.get('values', [])
        
        # If first row is empty, add headers
        if not values:
            headers = [['From', 'Subject', 'Date', 'Content']]
            
            # Write headers to the sheet
            service.spreadsheets().values().update(
                spreadsheetId=config.SPREADSHEET_ID,
                range=f"'{config.SHEET_NAME}'!A1:D1",
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            print('Headers created in Google Sheet.')
        else:
            print('Headers already exist.')
        
        return True
    
    except HttpError as error:
        print(f'Error setting up headers: {error}')
        return False


def append_email_to_sheet(service, email_data):
  
    try:

        row = [
            email_data.get('from', ''),
            email_data.get('subject', ''),
            email_data.get('date', ''),
            email_data.get('content', '')
        ]
        
        # Wrapping it in another list 
        values = [row]
        
        # Appendding to the sheet
        result = service.spreadsheets().values().append(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"'{config.SHEET_NAME}'!A:D",  # Use single quotes around sheet name for spaces
            valueInputOption='RAW',            
            insertDataOption='INSERT_ROWS',    
            body={'values': values}
        ).execute()
        
        print(f"Email added to sheet: {email_data.get('subject')}")
        return True
    
    except HttpError as error:
        print(f'Error appending to sheet: {error}')
        return False


def get_all_emails_from_sheet(service):
 
    try:
        # It will read all data from the sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=config.SPREADSHEET_ID,
            range=f"'{config.SHEET_NAME}'!A:D"  # Use single quotes around sheet name for spaces
        ).execute()
        
        values = result.get('values', [])
        
        # If empty or only headers
        if not values or len(values) <= 1:
            return []
        
        # Convert rows to dictionaries 
        emails = []
        for row in values[1:]:  # Skipping header row
      
            email = {
                'from': row[0] if len(row) > 0 else '',
                'subject': row[1] if len(row) > 1 else '',
                'date': row[2] if len(row) > 2 else '',
                'content': row[3] if len(row) > 3 else ''
            }
            emails.append(email)
        
        return emails
    
    except HttpError as error:
        print(f'Error reading from sheet: {error}')
        return []