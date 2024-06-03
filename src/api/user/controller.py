"""Controller personalizado user."""
from sqlalchemy import select

from communs.base_model import AbstractBaseModel
from communs.generic_controller import GenericController
from communs.security import get_password_hash
from database.session import Session
from models.user import User


class UserController(GenericController):
    """Controller for User."""

    def __init__(self) -> None:
        """Initialize the controller."""
        super().__init__(User)

    def get_user_by_username(self, db_session: Session, username: str) -> User:
        """Get user by username."""
        return db_session.scalar(select(User).where(User.username == username))

    def save(self, db_session: Session, obj: User) -> AbstractBaseModel:
        """Save user."""
        obj.password = get_password_hash(obj.password)
        print(obj.password)   # TODO: Remover
        return super().save(db_session, obj)

    def update(self, db_session: Session, obj: User) -> AbstractBaseModel:
        """Update user."""
        obj.password = get_password_hash(obj.password)
        return super().update(db_session, obj)
