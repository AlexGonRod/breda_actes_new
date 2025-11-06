import reflex as rx
from ..components.image_uploader import image_uploader

def factures():
    return rx.container(
            image_uploader(),
            display="flex",
            justify_content="center",
            align_items="center",
            width="100vw"
            )
