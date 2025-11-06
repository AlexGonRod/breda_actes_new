import reflex as rx
from .lib import copy

from .pages.formulary import formulari
from .pages.uploader import factures


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.heading("Benviguts a la pàgina de la Breda de l'Eixample!", size="8", text_align="center"),
            rx.list.ordered(
                rx.foreach(copy.copy, lambda item: rx.list.item(item, margin_bottom="5px")),
            ),
            rx.link(
                rx.button("D'acord"),
                href="/formulari",
                margin="0 auto"
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )

app = rx.App()
app.add_page(index)
app.add_page(formulari, route="/formulari", title="Formulari de la Breda")
app.add_page(factures, route="/factures", title="Factures")
