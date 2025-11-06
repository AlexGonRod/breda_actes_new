import reflex as rx
from ..components.wrapper  import wrapper
from ..lib.google import GoogleSheets
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_SPREADSHEET_ID=os.getenv("GOOGLE_ACTES_SPREADSHEET_ID") or ""
GOOGLE_SHEET = "Paellas 2025"


class FormState(rx.State):
    form_data: dict = {}
    loading: bool = False


    async def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.loading = True
        yield

        try:
            GoogleSheets(GOOGLE_SPREADSHEET_ID, GOOGLE_SHEET).append_row(list(form_data.values()))
            self.loading = False
            yield rx.toast.success(f"✅ Reserva enviada correctament", duration=3000, position="top-center")

        except Exception as e:
            self.loading = False
            message = e.message if hasattr(e, 'message') else str(e)
            yield rx.toast.error(f"❌ Error enviant la reserva: {message}", duration=5000, position="top-center")


def formulari():
    return rx.container(
            wrapper(),
            rx.form(
                rx.vstack(
                    rx.form.field(
                        rx.form.label("Formulari del Concurs de paelles", font_size="24px", font_weight="bold", margin_bottom="16px"),
                        rx.flex(
                            rx.form.label("Nombre"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Nom i cognoms",
                                    type="text",
                                    required=True
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "El nom és obligatori",
                                match="valueMissing",
                                color="red"
                            ),
                            rx.form.message(
                                "El nom és obligatori",
                                match="typeMismatch",
                                color="red"
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="nom",
                        width="100%",
                    ),
                    rx.form.field(
                        rx.flex(
                            rx.form.label("telefon"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Telèfon",
                                    type="number",
                                    pattern="[0-9]{9,}",
                                    required=True
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "El telèfon és obligatori",
                                match="valueMissing",
                                color="red"
                            ),
                            rx.form.message(
                                "El telèfon no és vàlid",
                                match="patternMismatch",
                                color="orange"
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="telefon",
                        width="100%",
                    ),
                    rx.form.field(
                        rx.flex(
                            rx.form.label("persones"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Participants",
                                    type="number",
                                    required=True
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "Aquest camp és obligatori",
                                match="valueMissing",
                                color="red"
                            ),
                            rx.form.message(
                                "Aquest camp és obligatori",
                                match="typeMismatch",
                                color="red"
                            ),
                            direction="column",
                            spacing="1",
                            width="100%"
                        ),
                        name="nombre",
                        width="100%",
                    ),
                    rx.button("Submit",rx.spinner(loading=FormState.loading), disable=FormState.loading, type="submit", width="100%"),

                ),
                on_submit=FormState.handle_submit,
                reset_on_submit=True,

                border="1px solid",
                border_radius="10px",
                padding="20px",
                spacing="15px",
            ),
            rx.divider(),
    )
