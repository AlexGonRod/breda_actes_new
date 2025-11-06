import reflex as rx
from ..lib.gemini import Gemini

class State(rx.State):
    """The app state."""

    # The images to show.
    img: list[str] = []
    gemini_response:dict = {}

    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.name

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.name)

        try:
            response = Gemini(self.img).get_result()
            self.gemini_response = response[0]
            print(self.gemini_response)
        except Exception as e:
            raise Exception(f"Error al procesar la imatge {str(e)}")


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
                State.img,
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
