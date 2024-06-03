"""Esquemas de validação para os tokens JWT."""
from pydantic import BaseModel


class AccessToken(BaseModel):
    """Representao o token JWT."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Repres. os dados do usuário logado dentro do token JWT (access_token)."""

    username: str | None = None  # noqa: FA102
