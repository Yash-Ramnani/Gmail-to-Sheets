# Google API scopes - what permissions we need
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',      
    'https://www.googleapis.com/auth/gmail.modify',        
    'https://www.googleapis.com/auth/spreadsheets'         
]

CREDENTIALS_FILE = '../credentials/credentials.json'  
TOKEN_FILE = '../token.json'                          
STATE_FILE = '../processed_emails.txt'                

# Google Sheets settings
SPREADSHEET_ID = '17o-C3BvpCpQKNzfuzVXr-w2mXpYVfKWNfRooumWDw5U'  
SHEET_NAME = 'Sheet1'                        

# Email settings
MAX_RESULTS = 50  # How many emails it will fetch