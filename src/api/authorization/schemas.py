"""Autorization model schema module."""
from pydantic import BaseModel

from communs.base_model_schema import (
    BaseAuditDTOSchema,
    BaseAuditModelSchema,
)


class AuthorizationDTOSchema(BaseAuditDTOSchema):
    """Schema de Autorização."""

    role_id: int
    transaction_id: int


class AuthorizationSchema(AuthorizationDTOSchema, BaseAuditModelSchema):
    """Schema de Autorização."""

    id: int


class AuthorizationListSchema(BaseModel):
    """Schema de Autorização."""

    authorizations: list[AuthorizationSchema]  # noqa: FA102
