import reflex as rx

tailwind_config = {
    "theme": {
        "extend": {
            "colors": {
                "white": "#ffffff",
                "secondary": "#F9FBFA",
            }
        }
    },
}

config = rx.Config(
    app_name="breda_py",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
