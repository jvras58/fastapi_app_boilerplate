"""Base model schema module."""

from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    """Base model schema class."""

    id: int
