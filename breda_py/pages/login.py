import reflex as rx
from ..services.supabase_service import SupabaseService
from ..state.auth_state import AuthState

class FormState(rx.State):
    loading: bool = False

    @rx.event
    async def submit_form(self, form_data: dict):
        email: str = form_data["email"]
        password: str = form_data["password"]

        try:
            self.loading = True
            yield

                # Obtener el estado global de autenticación
            auth = await self.get_state(AuthState)

            response = SupabaseService().signin(email, password)
            if response and response.session:
                # Guardar token en el estado (se persiste automáticamente)
                auth.token = response.session.access_token

                yield rx.toast.success(
                    "✅ Login exitoso",
                    duration=3000,
                    position="top-center"
                )

                # Redirigir a factures
                yield rx.redirect("/factures")

        except Exception as e:
            message = e.message if hasattr(e, 'message') else str(e)
            yield rx.toast.error(f"❌ Error during login: {message}", duration=5000, position="top-center")
            raise Exception(f"❌ Error during login: {message}")
        finally:
            self.loading = False
            yield


def login_page():
    return rx.container(
            rx.heading("Login Page", font_size="24px", font_weight="bold", margin_bottom="16px"),
            rx.form(
                rx.form.field(
                    rx.form.label("email"),
                    rx.form.control(
                        rx.input(
                            placeholder="Correu electrònic",
                            type="email",
                            required=True,
                            name="email"
                        ),
                        as_child=True,
                    ),
                    rx.form.message(
                        "Obligatori",
                        match="valueMissing",
                        color="red"
                    ),
                ),
                rx.form.field(
                    rx.form.label("contrasenya"),
                    rx.form.control(
                        rx.input(
                            placeholder="La vostra contrasenya",
                            type="password",
                            required=True,
                            name="password"
                        ),
                        as_child=True,
                    ),
                    rx.form.message(
                        "Obligatori",
                        match="valueMissing",
                        color="red"
                    ),
                ),
                rx.button("Submit",rx.spinner(loading=FormState.loading), disable=FormState.loading, type="submit", width="100%"),
                on_submit=FormState.submit_form,
                reset_on_submit=True,
            ),
            spacing="15px",
        )


