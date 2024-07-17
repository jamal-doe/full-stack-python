import asyncio
import reflex as rx
from datetime import datetime, timezone
from sqlmodel import Field
import sqlalchemy
from .. import utils


class ContactEntryModel(rx.Model, table=True):
    user_id: int | None = None
    first_name: str
    last_name: str | None = None
    email: str | None = None
    message: str
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False
    )
