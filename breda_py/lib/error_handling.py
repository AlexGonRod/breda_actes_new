

class ErrorHandlerBase(Exception):
    def __init__(self, msg:str):
        self.message = msg;
        super().__init__(self.message)

class PermissionDenied(BaseException):
    def __init__(self, msg:str):
        super().__init__(f"Permiso denegado: {msg}")

class WorksheetNotFound(ErrorHandlerBase):
    def __init__(self, work_sheet:str):
        super().__init__(f"Worksheet no encontrada: '{work_sheet}'" if work_sheet else "Worksheet no especificada")

class SpreadsheetNotFound(ErrorHandlerBase):
    def __init__(self, spreadsheet_id:str):
        super().__init__(f"Spreadsheet no encontrada: '{spreadsheet_id}'" if spreadsheet_id else "Spreadsheet no especificada")

class APIError(ErrorHandlerBase):
    def __init__(self, msg:str):
        super().__init__(f"Error de API: {msg}")

class dataAppendError(ErrorHandlerBase):
    def __init__(self, msg:str):
        super().__init__(f"Error al añadir datos: {msg}")


