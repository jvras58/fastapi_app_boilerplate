"""Base model schema module."""
from datetime import datetime

from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    """Base model schema class."""

    id: int

class BaseAuditDTOSchema(BaseModel):
    """Schema de Auditoria."""

    audit_user_ip: str | None = None  # noqa: FA102
    audit_user_login: str | None = None  # noqa: FA102


class BaseAuditModelSchema(BaseModel):
    """Schema de Auditoria."""

    audit_created_at: datetime
    audit_updated_on: datetime
