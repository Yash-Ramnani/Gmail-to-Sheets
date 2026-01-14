import os.path
import config
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def authenticate_gmail():
   
    # creds will store our login information
    creds = None
    
    # Check if we've logged in before (token.json stores our previous login)
    if os.path.exists(config.TOKEN_FILE):
        # pickle.load reads saved data from a file
        with open(config.TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If we don't have valid credentials, we need to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # If login expired then refresh it
            creds.refresh(Request())
        else:
            # First time login - opens browser for you to sign in
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the login for next time (so you don't have to log in again)
        with open(config.TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    # Build and return the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_unread_emails(service, max_results=None):
   
    if max_results is None:
        max_results = config.MAX_RESULTS
    
    try:
        # Call Gmail API to list messages
        results = service.users().messages().list(
            userId='me',              
            q='is:unread in:inbox',   
            maxResults=max_results
        ).execute()
        
        #list of messages
        messages = results.get('messages', [])
        
        # If no unread emails found
        if not messages:
            print('No unread emails found.')
            return []
        
        return messages
    
    except HttpError as error:
        # If something goes wrong with the api call
        print(f'An error occurred: {error}')
        return []


def get_email_details(service, msg_id):
       
    try:
        # Get the full message by its ID
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'  
        ).execute()
        
        return message
    
    except HttpError as error:
        print(f'An error occurred fetching email {msg_id}: {error}')
        return None


def mark_email_as_read(service, msg_id):

    try:
        # Modify the message to remove the UNREAD label
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        
        print(f'Marked email {msg_id} as read.')
        return True
    
    except HttpError as error:
        print(f'Error marking email as read: {error}')
        return False