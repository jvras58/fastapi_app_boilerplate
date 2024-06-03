"""Controller module for Authorization API."""

from sqlalchemy import Select, and_, select

from api.user.controller import UserController
from communs.exceptions import (
    AmbiguousAuthorizationException,
    CredentialsValidationException,
    IllegalAccessExcetion,
)
from database.session import Session
from models.assignment import Assignment
from models.authorization import Authorization
from models.role import Role
from models.transaction import Transaction
from models.user import User

user_controller = UserController()


def validate_transaction_access(
    db_session: Session, current_user: User, op_code: str,
) -> None:
    """Validate if the user has access to the transaction."""
    if not current_user:
        raise CredentialsValidationException

    trasactions = get_user_authorized_transactions(db_session,
    current_user.id, op_code)
    if not trasactions:
        raise IllegalAccessExcetion(current_user.id, op_code)

    if len(trasactions) > 1:
        raise AmbiguousAuthorizationException(current_user.id, op_code)

    if trasactions[0].operation_code != op_code:
        raise IllegalAccessExcetion(current_user.id,
        trasactions[0].operation_code)


def get_user_authorized_transactions(
    db_session: Session, user_id: int,
    op_code: str = None,  # noqa: RUF013
) -> list[Transaction]:  # noqa: FA102
    """Get the transactions authorized to the user."""
    query: Select = (
        select(Transaction).join(Authorization).join(Role).join(Assignment).join(User)
    )

    criteria_and = []
    criteria_and.append(User.id == user_id)

    if op_code:
        criteria_and.append(Transaction.operation_code == op_code)

    query = query.filter(and_(*criteria_and))

    trasactions: list[Transaction] = db_session.scalars(query).all()
    return trasactions
