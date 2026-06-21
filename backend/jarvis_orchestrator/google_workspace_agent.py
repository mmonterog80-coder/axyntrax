import os
import pickle
import logging
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

# Scopes para leer, redactar y modificar correos, y leer/escribir eventos de calendario
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'
]

class GoogleWorkspaceAgent:
    def __init__(self, credentials_file='C:/AXYNTRAX/credentials.json', token_file='C:/AXYNTRAX/token.pickle'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.gmail_service = None
        self.calendar_service = None

    def authenticate(self):
        """Autenticación OAuth 2.0. Requiere interacción del usuario la primera vez."""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
                
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Error refrescando token: {e}")
                    self.creds = None

            if not self.creds:
                if not os.path.exists(self.credentials_file):
                    logger.warning(f"CRÍTICO: No se encuentra {self.credentials_file}. No se puede conectar a la Bóveda de Correos ni al Calendario.")
                    return False
                
                logger.info("Iniciando flujo de autenticación OAuth para mmonterog80@gmail.com...")
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                # Ejecutar el servidor local para el callback
                self.creds = flow.run_local_server(port=0)
                
            # Guardar el token para la próxima vez
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
                
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        logger.info("✅ Conexión establecida con la Bóveda de Google Workspace.")
        return True

    def get_upcoming_events(self, max_results=5):
        if not self.calendar_service:
            return []
        import datetime
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indica UTC
        events_result = self.calendar_service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def get_unread_emails(self, max_results=5):
        if not self.gmail_service:
            return []
        results = self.gmail_service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
        messages = results.get('messages', [])
        return messages

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    agent = GoogleWorkspaceAgent()
    if agent.authenticate():
        print("Autenticación exitosa. Bóveda operativa.")
    else:
        print("Requiere archivo credentials.json para iniciar Protocolo Mark VII.")
