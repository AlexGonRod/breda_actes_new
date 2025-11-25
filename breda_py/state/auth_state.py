import reflex as rx
from ..services.supabase_service import SupabaseService

class AuthState(rx.State):
    # Usar LocalStorage para persistencia automática
    token: str = rx.LocalStorage("")

    @rx.event
    def check_login(self):
        """Verifica si está autenticado, si no redirige a login"""
        if not self.is_authenticated:
            return rx.redirect("/login")

    def logout(self):
        """Cierra sesión y limpia el token"""
        self.token = ""
        return rx.redirect("/login")

    @rx.var
    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado"""
        return bool(self.token and self.token != "")
