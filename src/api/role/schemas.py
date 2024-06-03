"""Schema de papeis."""
from pydantic import BaseModel

from communs.base_model_schema import (
    BaseAuditDTOSchema,
    BaseAuditModelSchema,
)


class RoleDTOSchema(BaseAuditDTOSchema):
    """Representa um Role (Papel) para o sistema."""

    name: str
    description: str


class RoleSchema(RoleDTOSchema, BaseAuditModelSchema):
    """Representa um Role (Papel) para o sistema."""

    id: int


class RoleListSchema(BaseModel):
    """Representa uma lista de Roles (Papeis) para o sistema."""

    roles: list[RoleSchema]  # noqa: FA102
