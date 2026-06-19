import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify"
]

CREDENTIALS_FILE = "C:\\AXYNTRAX\\credentials.json"
TOKEN_FILE = "C:\\AXYNTRAX\\token.json"

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"Missing {CREDENTIALS_FILE}. Please download it from Google Cloud Console.")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def list_unread_messages(service):
    try:
        results = service.users().messages().list(userId='me', q="is:unread", maxResults=5).execute()
        messages = results.get('messages', [])
        
        parsed_msgs = []
        if not messages:
            return []
        
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'From']).execute()
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin asunto')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
            snippet = msg_data.get('snippet', '')
            parsed_msgs.append({
                "id": msg['id'],
                "from": from_email,
                "subject": subject,
                "snippet": snippet
            })
        return parsed_msgs
    except Exception as e:
        print(f"Error listing messages: {e}")
        return []

def create_draft(service, to_email, subject, body_text):
    try:
        message = EmailMessage()
        message.set_content(body_text)
        message["To"] = to_email
        message["From"] = "me"
        message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}
        
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        return draft
    except HttpError as error:
        print(f"An error occurred drafting: {error}")
        return None
