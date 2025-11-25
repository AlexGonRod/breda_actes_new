import reflex as rx
from ..components.image_uploader import image_uploader
from ..state.auth_state import AuthState


def factures():
    return rx.fragment(
        rx.cond(
            AuthState.is_authenticated,
            # Usuario autenticado - mostrar contenido
            rx.container(
                image_uploader(),
                display="flex",
                justify_content="center",
                align_items="center",
                width="100vw",
                on_mount=AuthState.check_login  # Verificar también aquí por si acaso
            ),
            # Usuario NO autenticado - mostrar loading y redirigir
            rx.container(
                rx.center(
                    rx.vstack(
                        rx.text(
                            "No estás registrado, redireccionando...",
                            font_size="18px",
                            color="gray.600"
                        ),
                        rx.spinner(size="3"),
                        spacing="3"
                    )
                ),
                height="100vh",
                display="flex",
                align_items="center",
                justify_content="center"
            )
        ),
        on_mount=AuthState.check_login  # Verificar al montar el fragment
    )
