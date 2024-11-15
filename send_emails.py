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
