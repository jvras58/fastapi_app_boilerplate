"""Schemas para a API de Designação de Usuários para Papéis."""

from pydantic import BaseModel

from communs.base_model_schema import (
    BaseAuditDTOSchema,
    BaseAuditModelSchema,
)


class AssignmentDTOSchema(BaseAuditDTOSchema):
    """Representa uma Designação de um usuário para um papel."""

    user_id: int
    role_id: int


class AssignmentSchema(AssignmentDTOSchema, BaseAuditModelSchema):
    """Representa uma Designação de um usuário para um papel."""

    id: int


class AssignmentListSchema(BaseModel):
    """Representa uma lista de Designações de Usuários para Papéis."""

    assignments: list[AssignmentSchema]  # noqa: FA102
