import gspread
from google.oauth2.service_account import Credentials
import os
from ..error_handling import PermissionDenied, SpreadsheetNotFound

from dotenv import load_dotenv

load_dotenv()

credentials = {
    "type": os.getenv("GOOGLE_TYPE"),
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY"),
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN"),
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(credentials, scopes=SCOPES)

# Validar que todas las credenciales se cargaron
missing = [k for k, v in credentials.items() if v is None]
if missing:
    raise PermissionDenied(f"Faltan cedenciales: {missing}")

class GoogleClient:
    def __init__(self, spreadhseet_name: str, sheet_name: str):
        print(spreadhseet_name, sheet_name)

        # authorize the clientsheet
        try:
            self.client = gspread.Client(auth=creds)

            # get the instance of the Spreadsheet
            self.ws = self.client.open_by_key(spreadhseet_name)
            self.sheet = self.ws.worksheet(sheet_name)

            if not self.sheet:
                raise SpreadsheetNotFound(f"{spreadhseet_name}")

            self.last_row = self.sheet.row_count
        except Exception as e:
            raise Exception(f'Error initializing GoogleClient: {str(e)}')

