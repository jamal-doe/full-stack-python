import asyncio
import reflex as rx
from .. import navigation
from ..ui.base import base_page
from datetime import datetime, timezone
from sqlmodel import Field
import sqlalchemy


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ContactEntryModel(rx.Model, table=True):
    first_name: str
    last_name: str | None = None
    email: str | None = None
    message: str
    timestamp: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )


class ContactState(rx.State):
    form_data: dict = {}
    did_submit: bool = False

    async def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        print(form_data)
        self.form_data = form_data
        data = {}
        for key, value in form_data.items():
            if value == "" or value is None:
                continue
            data[key] = value
        with rx.session() as session:
            db_entry = ContactEntryModel(**data)
            session.add(db_entry)
            session.commit()
        self.did_submit = True
        yield
        await asyncio.sleep(2)
        self.did_submit = False
        yield

    @rx.var
    def thank_you(self):
        """Return a thank you message."""
        first_name = self.form_data.get("first_name") or ""
        return f"Thank You {first_name}".strip() + "!"


@rx.page(route=navigation.routes.CONTACT_US_ROUTE)
def contact_page() -> rx.Component:
    my_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="first_name",
                    placeholder="First Name",
                    required=True,
                    type="text",
                    width="100%",
                ),
                rx.input(
                    name="last_name",
                    placeholder="Last Name",
                    type="text",
                    width="100%",
                ),
                width="100%",
            ),
            rx.input(
                name="email",
                placeholder="your@email.com",
                required=False,
                type="email",
                width="100%",
            ),
            rx.text_area(
                name="message",
                placeholder="Your message",
                required=True,
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=ContactState.handle_submit,
        reset_on_submit=True,
    ),
    my_child = rx.vstack(
        rx.heading("Contact Us", size="9"),
        rx.cond(ContactState.did_submit, ContactState.thank_you, ""),
        rx.desktop_only(
            rx.box(
                my_form,
                id='my-form-box',
                width="40vw",
            ),
        ),
        rx.tablet_only(
            rx.box(
                my_form,
                width="60vw",
            ),
        ),
        rx.mobile_only(
            rx.box(
                my_form,
                width="80vw",
            ),
        ),
        spacing="5",
        justify="center",
        align="center",
        min_height="80vh",
        id='my-child'
    )
    return base_page(my_child)
