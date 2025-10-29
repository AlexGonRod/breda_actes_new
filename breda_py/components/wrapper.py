import reflex as rx

def wrapper() -> rx.Component:
    return rx.flex(
                rx.text("🥘", size="9", align="center", margin=""),
                rx.heading("Concurs de paelles", as_="h1", size="8", align="center"),
                rx.heading("Breda de l'Eixample", as_="h2", size="6", align="center", margin_bottom="16px"),
                rx.text("Si us plau, ompliu el formulari per participar en el concurs de paelles."),
                rx.text("Qualsevol dubte, posseu-vos en contacte a: ", rx.link("bredainfocat@gmail.com ", href="mailto:bredainfocat@gmail.com")),
                border="1px solid",
                border_radius="10px",
                padding="20px",
                margin_bottom="20px",
                direction="column",
                spacing="1",
                width="100%",
                # class_name="bg-white text-black",
            )
