import reflex as rx
from ..lib.gemini import Gemini
from ..lib.googleSheets import GoogleSheets
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
GOOGLE_FACTURES_SPREADSHEET_ID=os.getenv("GOOGLE_FACTURES_SPREADSHEET_ID") or ""
GOOGLE_SHEET = "2-JUSTIFICACIO_RELACIO DESPESES"


class State(rx.State):
    """The app state."""

    data_img: list[str] = []
    images: list[str] = []
    gemini_response: list= []
    loading: bool = False
    path = rx.get_upload_dir()


    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):

        for file in files:
            upload_data = await file.read()
            outfile = self.path / file.name

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.data_img.append(file.name if file.name else "")
            self.images.append(file.name if file.name else "")

        try:
            self.gemini_response = Gemini(self.data_img).get_result()

        except Exception as e:
            raise Exception(f"Error al procesar la imatge {str(e)}")

        try:
            self.loading = True
            yield

            response = GoogleSheets(GOOGLE_FACTURES_SPREADSHEET_ID, GOOGLE_SHEET).append_row(self.gemini_response)
            if response is not None:
                self.data_img = []
                self.loading = False
                yield rx.toast.success(f"✅ Dades enviades correctament", duration=3000, position="top-center")

        except Exception as e:
            self.loading = False
            message = e.message if hasattr(e, 'message') else str(e)
            print(f"❌ Error enviant dades: {message}")
            yield rx.toast.error(f"❌ Error enviant dades: {message}", duration=5000, position="top-center")


def image_uploader():
    """The main view."""
    return rx.vstack(
        rx.upload(
            rx.box(
                rx.icon(
                tag="cloud_upload",
                style={
                    "width": "3rem",
                    "height": "3rem",
                    "color": "#2563eb",
                    "marginBottom": "0.75rem",
                },
            ),
                rx.hstack(
                rx.text(
                    "Clica per pujar una imatge",
                    style={"fontWeight": "bold", "color": "#1d4ed8"},
                ),
            ),
                rx.text(
                "SVG, PNG, JPG or GIF (MAX. 5MB)",
                style={"fontSize": "0.75rem", "color": "#6b7280", "marginTop": "0.25rem"},
            ),
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "1.5rem",
                    "textAlign": "center",
                },
            ),
            id="upload2",
            multiple=True,
            disabled=False,
            max_files=5,
            accept={
                "application/pdf": [".pdf"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
            },
            no_keyboard=True,
            on_drop=State.handle_upload(
                rx.upload_files(upload_id="upload2")
            ),
        ),
        rx.grid(
            rx.foreach(
                State.images,
                lambda img: rx.vstack(
                    rx.image(src=rx.get_upload_url(img),
                                border_radius="8px",
                                width= "90px",
                                box_sizing= "border-box",
                                height= "90px",
                                object_fit= "cover",
                            ),
                rx.text(img, max_width="100px", text_align="center", font_size="sm", white_space="nowrap", overflow="hidden", text_overflow="ellipsis"),
                    align_items="center",
                    spacing="2",
                ),
            ),
            columns="3",
            spacing="4",
            margin_top="1rem",

        ),
    )
