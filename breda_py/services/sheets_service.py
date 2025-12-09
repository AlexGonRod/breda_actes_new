import gspread
from ..lib.error_handling import (WorksheetNotFound, SpreadsheetNotFound, APIError, dataAppendError, PermissionDenied)
from .google_clients.google_client import GoogleClient
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_FACTURES_SPREADSHEET_ID=os.getenv("GOOGLE_FACTURES_SPREADSHEET_ID") or ""
GOOGLE_SHEET_DADES = "4-RELACIO_DESPESES_PER_UNITAT"

class FORMDATA:
    nombre: str;
    telefon: int;
    persones: int;

class FACTURADATA(TypedDict):
    num_de_documento: str;
    fecha: str;
    proveedor:str;
    NIF_CIF: str;
    tipo_material: str;
    total: str;
    lineas: list[dict];

def mockData(factures: list[FACTURADATA]) -> tuple[list, list]:
    mockedBill: list = [];
    mockedUnit: list = [];
    for factura in factures:
        mockedBill.append([
            "Factura",  # Tipus de document (puedes ajustar según el caso)
            factura.get("num_de_documento", ""),
            factura.get("fecha", ""),
            factura.get("proveedor", ""),
            factura.get("NIF_CIF", ""),
            "",  # Objecte de les factures
            factura.get("total", ""),
            "100,00%",
        ])
        for linea in factura["lineas"]:
            mockedUnit.append([
                factura.get("num_de_documento", ""),
                factura.get("proveedor", ""),
                factura.get("fecha", ""),
                linea.get("concepto", ""),
                linea.get("cantidad", ""),
                linea.get("precio_unitario", ""),
                linea.get("importe", ""),
            ])
    return mockedBill, mockedUnit


BLOCKS = [
    {"start": 17, "end": 36},   # Primer bloque
    {"start": 57, "end": 76}    # Segundo bloque
]

def get_first_empty_row(sheet, start, end, col=2):
    cell_range = f"{chr(64+col)}{start}:{chr(64+col)}{end}"  # Ejemplo: "B17:B20"
    values = sheet.get(cell_range)

    for i, row in enumerate(values):
        if not row or row == ['']:
            return start + i
    if len(values) < (end - start + 1):
        print(f"First empty row in block {start}-{end} is {start + len(values)}")
        return start + len(values)
    return None  # bloque lleno

def append_data_row(data:list[FACTURADATA]) -> tuple[bool, str]:
    client = GoogleClient(GOOGLE_FACTURES_SPREADSHEET_ID, GOOGLE_SHEET_DADES)

    print(f"client.last_row+1: {client.last_row+1}")
    try:
        for item in data:
            print(f"item: {item}")
            datamocked = [item[0], item[1], item[2], item[3], item[4], item[5]]
            client.sheet.append_row(datamocked, table_range=f"A{client.last_row+1}")
        return (True, "Unidades añadidos correctamente")
    except gspread.exceptions.WorksheetNotFound:
        raise WorksheetNotFound(f"{client.ws}")

class SheetsService:
    def __init__(self, spreadsheet_name: str, sheet_name: str):
        # authorize the clientsheet
        self.client = GoogleClient(spreadsheet_name, sheet_name)
        self.spreadsheet_name = spreadsheet_name
        self.sheet_name = sheet_name
        self.data_mock = []
        self.data_mock2 = []

    def __mock_formdata__(self, data):
        return self.client.last_row+1,data[0], data[1], data[2]

    def append_row(self, data: list[FORMDATA] | list[FACTURADATA], type: str = "") -> tuple[bool, str]:
        if not data:
            raise dataAppendError("No hay datos para añadir")

        # FORMULARI
        if type == "formdata":
            try:
                self.data_mock = self.__mock_formdata__(data)
                self.client.sheet.append_row(self.data_mock, table_range=f"A{self.client.last_row+1}")
            except gspread.exceptions.WorksheetNotFound:
                raise WorksheetNotFound(f"{self.client.ws}")

        # FACTURES
        self.data_mock, self.data_mock2 = mockData(data)
        remaining = self.data_mock.copy()
        batch_updates = []

        for block in BLOCKS:
            start, end = block["start"], block["end"]
            first_empty = get_first_empty_row(self.client.sheet, start, end)

            if first_empty is None:
                print(f"🟩 Bloque {start}-{end} lleno. Pasando al siguiente bloque.")
                continue  # bloque lleno, pasa al siguiente

            available_space = end - first_empty + 1
            to_write = remaining[:available_space]
            remaining = remaining[available_space:]

            # Rango dinámico para escribir
            start_range = f"B{first_empty}"
            end_range = f"K{first_empty + len(to_write) - 1}"
            range_a1 = f"{start_range}:{end_range}"

            print(f"✍️ Escribiendo {len(to_write)} facturas en rango {range_a1}")
            batch_updates.append({
                "range": range_a1,
                "values": to_write
            })

            if not remaining:
                print(f"⚠️ No hay espacio suficiente para {len(remaining)} facturas restantes.")
                break

        if not batch_updates:
            print("⚠️ No hay espacio disponible para escribir.")
            return (False, "Sin espacio disponible")
    # return (True, "Datos añadidos correctamente")
        try:
            self.client.sheet.batch_update(batch_updates, value_input_option="USER_ENTERED")
            print(f"✅ Escrito {len(batch_updates)} bloque(s) en Google Sheets.")
            append_data_row(self.data_mock2)
            return (True, "Datos añadidos correctamente")

        except gspread.exceptions.WorksheetNotFound:
            raise WorksheetNotFound(f"{self.client.ws}")

        except gspread.exceptions.APIError as e:
            if e.response.status_code == 404:
                raise SpreadsheetNotFound(f"{self.client.sheet}")
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

