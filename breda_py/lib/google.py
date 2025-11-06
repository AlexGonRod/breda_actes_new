import gspread
import os
from google.oauth2.service_account import Credentials
from .error_handling import (WorksheetNotFound, SpreadsheetNotFound, APIError, dataAppendError, PermissionDenied)

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


class DATASTORE:
    nombre: str;
    telefon: int;
    persones: int;


class GoogleSheets:
    def __init__(self, spreadhseet_name: str, sheet_name: str):
        # authorize the clientsheet
            self.client = gspread.Client(auth=creds)

            # get the instance of the Spreadsheet
            self.ws = self.client.open_by_key(spreadhseet_name)
            self.sheet = self.ws.worksheet(sheet_name)

            if not self.sheet:
                raise SpreadsheetNotFound(f"{spreadhseet_name}")

            self.last_row = self.sheet.row_count

    def __mock_data__(self, data):
        return self.last_row-1, data[0], data[1], data[2]

    def append_row(self, data: list[DATASTORE]) -> tuple[bool, str]:
        print(f"Appending data to Google Sheets {self.sheet}: {data}")
        data_mock = self.__mock_data__(data)

        if not data:
            raise dataAppendError("No hay datos para añadir")

        try:
            self.sheet.append_row(data_mock, table_range=f"A{self.last_row+1}")
            return (True, f"Fila {self.last_row} añadida correctamente")

        except gspread.exceptions.WorksheetNotFound:
            raise WorksheetNotFound(f"{self.ws}")

        except gspread.exceptions.APIError as e:
            if e.response.status_code == 404:
                raise SpreadsheetNotFound(f"{self.sheet}")
            if e.response.status_code == 429:
                raise dataAppendError("Límite de cuota excedido")
            elif e.response.status_code == 403:
                raise PermissionDenied("Acceso denegado a la hoja de cálculo")
            else:
                raise APIError(f"Código de estado {e.response.status_code}")

        except gspread.exceptions.GSpreadException as e:
            return (False, f"Error al añadir datos: {str(e)}")

        except Exception as e:
            raise  PermissionDenied(f"Error: {str(e)}")

