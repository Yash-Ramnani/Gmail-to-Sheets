import base64
from datetime import datetime
from email.utils import parsedate_to_datetime


def get_header(headers, name):
    
    # Looping through headers to find the one we want
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    
    return ''  


def extract_email_body(payload):
    
    body = ''
    
    # If the email has multiple parts 
    if 'parts' in payload:
        for part in payload['parts']:
            # Look for plain text
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    
                    body = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
                    break
            # If part itself has parts means nested structure
            elif 'parts' in part:
                body = extract_email_body(part)
                if body:
                    break
    
    # If single part email
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(
            payload['body']['data']
        ).decode('utf-8')
    
    return body


def parse_email(message):

    # Get headers and payload from the message
    headers = message['payload']['headers']
    payload = message['payload']
    
    # Extract sender
    from_email = get_header(headers, 'From')
    
    # Extract subject
    subject = get_header(headers, 'Subject')
    
    # Extract date
    date_str = get_header(headers, 'Date')
    
    # Format the date nicely
    try:
        date_obj = parsedate_to_datetime(date_str)
        
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    except:
        # If date parsing fails then it will use the raw date string
        formatted_date = date_str
    
    # Extract email body
    content = extract_email_body(payload)
    
    # Clean up content 
    content = content.strip()
    
    
    # Return as a dictionary
    return {
        'id': message['id'],           
        'from': from_email,
        'subject': subject,
        'date': formatted_date,
        'content': content
    }