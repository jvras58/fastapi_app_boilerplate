"""Schemas for Transaction module."""
from pydantic import BaseModel

from communs.base_model_schema import (
    BaseAuditDTOSchema,
    BaseAuditModelSchema,
)


class TransactionDTOSchema(BaseAuditDTOSchema):
    """Data Transfer Object schema for Transaction."""

    name: str
    description: str
    operation_code: str


class TransactionSchema(TransactionDTOSchema, BaseAuditModelSchema):
    """Data Transfer Object schema for Transaction."""

    id: int


class TransactionListSchema(BaseModel):
    """Data Transfer Object schema for Transaction."""

    transactions: list[TransactionSchema]  # noqa: FA102
