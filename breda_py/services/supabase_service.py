import reflex as rx
from .supabase_client.supabase_client import SupabaseClient
from ..lib.error_handling import (dataAppendError, PermissionDenied)

class SupabaseService:
    def __init__(self):
        self.supabase = SupabaseClient()
        self.token: str = ""
        self.is_authenticated: bool = False

    def signin(self, email: str , password: str):
        self.email = email
        self.password = password

        if not self.email or not self.password:
            raise dataAppendError("Supabase: ")

        try:
            auth_response = self.supabase.client.auth.sign_in_with_password(
                {
                    "email": self.email,
                    "password": self.password,
                }
            )
            return auth_response

        except PermissionDenied as e:
            raise PermissionDenied(f"{str(e)}")




