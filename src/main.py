import os
import sys

# Adding the parent directory to the path so we can import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src import gmail_service, sheets_service, email_parser


def load_processed_emails():
      
    processed_ids = set() 
    
    # Checks if the state file exists
    if os.path.exists(config.STATE_FILE):
        try:
            with open(config.STATE_FILE, 'r') as f:
                for line in f:
                    # Add each ID to the set
                    processed_ids.add(line.strip())
            
            print(f'Loaded {len(processed_ids)} previously processed emails.')
        except Exception as e:
            print(f'Error loading state file: {e}')
    else:
        print('No previous state found. Starting fresh.')
    
    return processed_ids


def save_processed_email(email_id):

    try:
        with open(config.STATE_FILE, 'a') as f:
            f.write(email_id + '\n')  # Write ID with newline
    except Exception as e:
        print(f'Error saving email ID: {e}')


def main():
    
    print('=' * 60)
    print('Gmail to Sheets Automation Starting...')
    print('=' * 60)
    
    # Step 1: Authenticate with Gmail
    print('\n[1/6] Authenticating with Gmail...')
    try:
        gmail = gmail_service.authenticate_gmail()
        print('✓ Gmail authentication successful!')
    except Exception as e:
        print(f'✗ Gmail authentication failed: {e}')
        return
    
    # Step 2: Authenticate with Google Sheets
    print('\n[2/6] Authenticating with Google Sheets...')
    try:
        sheets = sheets_service.authenticate_sheets()
        print('✓ Sheets authentication successful!')
    except Exception as e:
        print(f'✗ Sheets authentication failed: {e}')
        return
    
    # Step 3: Setup sheet headers
    print('\n[3/6] Setting up Google Sheet headers...')
    sheets_service.setup_sheet_headers(sheets)
    
    # Step 4: Load processed emails state
    print('\n[4/6] Loading previous state...')
    processed_ids = load_processed_emails()
    
    # Step 5: Fetch unread emails
    print('\n[5/6] Fetching unread emails from Gmail...')
    messages = gmail_service.get_unread_emails(gmail)
    
    if not messages:
        print('No unread emails found. Nothing to process.')
        return
    
    print(f'Found {len(messages)} unread email(s).')
    
    # Step 6: Process each email
    print('\n[6/6] Processing emails...')
    print('-' * 60)
    
    new_emails_count = 0
    skipped_emails_count = 0
    
    for idx, message in enumerate(messages, 1):
        email_id = message['id']
        
        # Check if we've already processed this email
        if email_id in processed_ids:
            print(f'[{idx}/{len(messages)}] Skipping already processed email: {email_id}')
            skipped_emails_count += 1
            continue
        
        print(f'[{idx}/{len(messages)}] Processing email: {email_id}')
        
        # Get full email details
        full_message = gmail_service.get_email_details(gmail, email_id)
        
        if not full_message:
            print(f'  ✗ Failed to fetch email details')
            continue
        
        # Parse the email
        email_data = email_parser.parse_email(full_message)
        
        print(f'  From: {email_data["from"]}')
        print(f'  Subject: {email_data["subject"]}')
        print(f'  Date: {email_data["date"]}')
        
        # Add to Google Sheet
        success = sheets_service.append_email_to_sheet(sheets, email_data)
        
        if success:
            # Mark as read in Gmail
            gmail_service.mark_email_as_read(gmail, email_id)
            
            # Save to state file
            save_processed_email(email_id)
            processed_ids.add(email_id)  
            
            new_emails_count += 1
            print(f'  ✓ Email processed successfully!')
        else:
            print(f'  ✗ Failed to add email to sheet')
        
        print()
    
    # Summary
    print('=' * 60)
    print('Processing Complete!')
    print(f'New emails processed: {new_emails_count}')
    print(f'Already processed (skipped): {skipped_emails_count}')
    print(f'Total unread emails found: {len(messages)}')
    print('=' * 60)


# It will run the main function
if __name__ == '__main__':
    main()