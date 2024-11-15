## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    ## Prerequisites

- Python 3.6 or higher
- Google Cloud Platform account
- Gmail API enabled
- Required Python packages (see requirements.txt)

## Required Files

1. `credentials.json` - OAuth 2.0 credentials from Google Cloud Console
2. `contacts.xlsx` - Excel file with the following columns:
   - email: Recipient's email address
   - subject: Email subject line
   - message: Email body content
3. `config.json` - Configuration file (will be created during setup)

## Step-by-Step Solution

1. First, let's install the required packages:

```
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas
```

2. Here's a Python script that will help you accomplish this:

```
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
import pickle
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
  """Sets up and returns Gmail service"""
  creds = None
  
  # Check if token.pickle exists
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
          
  # If credentials are invalid or don't exist, let's create them
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
          
      # Save credentials for future use
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
  """Creates an email message"""
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
  """Sends an email message"""
  try:
      message = service.users().messages().send(
          userId=user_id, body=message).execute()
      print(f"Message Id: {message['id']}")
      return message
  except Exception as e:
      print(f"An error occurred: {e}")
      return None

def main():
  # Read the spreadsheet
  df = pd.read_excel('contacts.xlsx')  # or pd.read_csv('contacts.csv')
  
  # Get Gmail service
  service = get_gmail_service()
  
  # Your Gmail address
  sender = "your.email@gmail.com"
  
  # Iterate through the spreadsheet and send emails
  for index, row in df.iterrows():
      to = row['email']  # Assuming 'email' is the column name
      subject = row['subject']  # Assuming 'subject' is the column name
      message_text = row['message']  # Assuming 'message' is the column name
      
      # Create and send message
      message = create_message(sender, to, subject, message_text)
      send_message(service, 'me', message)
      print(f"Email sent to {to}")

if __name__ == '__main__':
  main()

# Created/Modified files during execution:
print("Files created/modified:")
for file in ["token.pickle"]:
  if os.path.exists(file):
      print(f"- {file}")
```

3. Spreadsheet Format

Your spreadsheet (contacts.xlsx or contacts.csv) should have these columns:

email: Recipient's email address

subject: Email subject

message: Email content

| email               | subject	      |message            |
|---------------------|---------------|-------------------|
| student1@mail.com   | subject line  | message.....      |
| student2@mail.com   | subject line  | message.....      |
| student3@mail.com   | subject line  | message.....      |

## Setup Instructions

## 1. Create a Google Cloud Project:
    
    -Go to Google Cloud Console
    
    -Create a new project
    
    -Enable Gmail API
    
    -Create OAuth 2.0 credentials
    
    -Download the credentials and save as credentials.json in your project directory

## 2. Prepare Your Data:

    -Create your spreadsheet with the required columns

    -Save it as 'contacts.xlsx' or 'contacts.csv' in your project directory

## 3. Run the Script:

    -First time you run it, it will open a browser window for authentication

    -Grant the necessary permissions

    -The script will create a token.pickle file for future use

## Next Steps After Code Setup

## 1. Prepare Your Files
You need three essential files in your project folder:

gmail_automation/

    ├── credentials.json    # From Google Cloud Console
    ├── contacts.xlsx      # Your test spreadsheet
    └── send_emails.py     # Your code (already done)


## 2. Get Google Credentials
Go to Google Cloud Console
Create/Select your project
Enable Gmail API
Create OAuth credentials
Download credentials.json
Place credentials.json in your project folder

## 3. Update Code

In send_emails.py, modify:

```
sender = "your.actual.email@gmail.com"  # Change to your Gmail" 
```

## 4. Test Run

Open terminal in your project folder

Run:

```
python send_emails.py
```

## 5. First-Time Authorization

    1. Browser will open

    2. Select your Google account

    3. Grant permissions

    4. A token.pickle file will be created

## Common Issues to Check:

✓ credentials.json is in the correct folder

✓ contacts.xlsx is properly formatted

✓ Your Gmail address is correctly specified in the code

✓ You're running the script from the correct directory
