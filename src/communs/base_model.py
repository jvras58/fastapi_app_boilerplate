"""Represent the base model for all models in the application."""

from dataclasses import dataclass

from sqlalchemy import DateTime, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base model for all models in the application."""


@dataclass
class AbstractBaseModel:
    """Auditable Base model for all models in the application."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(  # noqa: RUF009
        primary_key=True,
        init=False,
        autoincrement=True,
    )

    audit_user_login: Mapped[str] = mapped_column(  # noqa: RUF009
        String(30),
        name='audit_user_login',
        nullable=False,
    )
    audit_user_ip: Mapped[str] = mapped_column(  # noqa: RUF009
        String(16),
        name='audit_user_ip',
        nullable=False,
    )
    audit_created_at: Mapped[DateTime] = mapped_column(  # noqa: RUF009
        DateTime(timezone=True),
        name='audit_created_at',
        server_default=func.now(),
        nullable=False,
        init=False,
    )
    audit_updated_at: Mapped[DateTime] = mapped_column(  # noqa: RUF009
        DateTime(timezone=True),
        name='audit_updated_at',
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        init=True,
    )

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the model."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def get_updated_data(self, obj: 'AbstractBaseModel') -> None:
        """Update the model with the new data."""
        for key, value in obj._as_dict().items():  # noqa: SLF001
            setattr(self, key, value)

    def _as_dict(self, jump_immutable_fields: bool = True) -> dict:
        """Return the model as a dictionary. Excludind audit attributes.

        This method is used to serialize the model to prepare it for update
        model.
        """
        # This fields are handled by the database.
        immutable_fields = ['audit_created_at', 'audit_updated_at']
        return {
            attr.key: getattr(self, attr.key)
            for attr in self.__mapper__.column_attrs
            if jump_immutable_fields and attr.key not in immutable_fields
        }

    def __repr__(self) -> str:
        """Return the model representation."""
        return f'<{self.__class__.__name__} {self.id}>'
