"""Schemas de Users."""
from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    """Classe que representa o usuário do sistema."""

    username: str
    display_name: str
    email: EmailStr
    password: str
    audit_user_ip: str = None
    audit_user_login: str = None


class UserPublic(BaseModel):
    """Classe que representa o usuário do sistema a ser expostas."""

    id: int
    username: str
    display_name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    """Representa uma lista de Usuários do sistema."""

    users: list[UserPublic]  # noqa: FA102
