# Gmail to Sheets Automation



**Made by Yash Ramnani\*\*



---



## 🚀 Project Overview



This project automates the process of reading unread emails from Gmail and logging them into a Google Sheet using Python.  

It connects securely via OAuth 2.0, extracts key email details, and appends them as structured rows while ensuring zero duplicates.



### Pipeline Goal  

Gmail → Python → Google Sheets  

Clean architecture • secure auth • reliable state management



---



## 🧱 High-Level Architecture



Gmail Inbox (Unread Emails)

│

▼

Gmail API (OAuth 2.0)

│

▼

Python Script

├── Fetch unread emails

├── Parse sender, subject, date, body

├── Check duplicates

└── Mark emails as read

│

▼

Google Sheets API

│

▼

Google Sheet (Logged Data)



Data flows one-way from Gmail to Sheets, with a local state file acting as memory to prevent reprocessing.



---



## 🛠 Step-by-Step Setup Instructions



### Prerequisites



- Python 3.7+  

- Gmail account  

- Google Cloud project with:

&nbsp; - Gmail API enabled  

&nbsp; - Google Sheets API enabled  



---



### Installation



Clone the repository and install dependencies:



pip install -r requirement.txt



## Google Cloud Configuration



Create a project in Google Cloud Console



Enable:

Gmail API

Google Sheets API



Create OAuth credentials → Desktop App



Download credentials.json



Place it inside:

credentials/credentials.json



Configure Sheet ID



Open config.py and add:

SPREADSHEET\_ID = 'your-sheet-id-here'



Run the Project



cd src

python main.py



First run opens Google sign-in for consent.

Token is stored locally for future executions.



## Core Logic Explained



### OAuth Flow



Loads credentials.json

Opens Google consent screen

User grants Gmail + Sheets permissions

Access token is stored securely

No passwords stored = Google best practice



Duplicate Prevention Strategy



Unread Filter – only unread emails fetched

Local State File – processed IDs stored in processed\_emails.txt

In-Memory Set – fast runtime lookup



Even if the script runs 100 times → same mail never logged twice.



State Persistence



File Used:

processed\_emails.txt



### Why this approach?



Lightweight

No DB overhead

Easy debugging

Perfect for automation MVPs



## Challenges Faced



Email Body Extraction = Boss Level



Gmail API responses included:



Base64 encoding

Multipart MIME

HTML + plain text mix

Attachments in same payload



## Solution



Built recursive MIME parser

Safe Base64 decoding

HTML fallback cleaning

Handles real-world messy emails



## Limitations



Plain text processing only

Body trimmed to 1000 chars

Attachments ignored

Single Gmail account

Deleting state file may reprocess

Google API rate limits apply



## Project Structure



gmail-to-sheets/

├── src/

│   ├── gmail\_service.py

│   ├── sheets\_service.py

│   ├── email\_parser.py

│   └── main.py

├── credentials/

│   └── credentials.json   # not committed

├── requirement.txt

├── config.py

└── README.md



## Conclusion



This project delivers a secure, automated, and production-style Gmail → Sheets pipeline with:



OAuth 2.0 authentication

Clean modular architecture

Bulletproof duplicate handling

Real-world email parsing



Tested with live inbox data and performing like a champ.





Date: January 14, 2026  

Author: Yash Ramnani














