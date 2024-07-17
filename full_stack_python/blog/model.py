import reflex as rx
# from ..utils import timing
from datetime import datetime
from .. import utils
import sqlalchemy
from sqlmodel import Field


class BlogPostModel(rx.Model, table=True):
    # id = rx.Field(rx.Integer, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False
    )

    # def __str__(self):
    #     return self.title
    #
    # def __repr__(self):
    #     return f'<BlogPostModel: {self.title}>'
