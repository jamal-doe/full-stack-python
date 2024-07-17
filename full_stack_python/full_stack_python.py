"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from .ui.base import base_page
from . import navigation, pages, contact


# Define the index page
def index() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
        rx.heading("Black Street AI", size="9"),
        rx.text(
            "Get started by editing ",
            rx.code(f"{config.app_name}/{config.app_name}.py"),
            size="5",
        ),

        # Button
        rx.link(
            rx.button("About Us", size="3", variant="outline"),
            href=navigation.routes.ABOUT_US_ROUTE,
            # is_external=True,
        ),

        # Styling
        spacing="5",
        justify="center",
        text_align="center",
        align="center",
        min_height="80vh",

        # id
        id="my_child"
    )
    return base_page(my_child)


app = rx.App()
app.add_page(index)
app.add_page(pages.about_page, route=navigation.routes.ABOUT_US_ROUTE)
app.add_page(pages.pricing_page, route=navigation.routes.PRICING_ROUTE)
app.add_page(contact.contact_page, route=navigation.routes.CONTACT_US_ROUTE)
app.add_page(
    contact.contact_entries_list_page,
    route=navigation.routes.CONTACT_ENTRIES_ROUTE,
    on_load=contact.ContactState.list_entries,
)
