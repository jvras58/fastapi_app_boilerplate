"""User router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS  # noqa: N812
from sqlalchemy.orm import Session

from api.authentication.controller import get_current_user
from api.authorization.controller import (
    get_user_authorized_transactions,
    validate_transaction_access,
)
from api.transaction.enum_operation_code import (
    EnumOperationCode as op,  # noqa: N813
)
from api.transaction.schemas import TransactionListSchema
from api.user.controller import UserController
from api.user.schemas import UserList, UserPublic, UserSchema
from communs.exceptions import (
    IntegrityValidationError as IntegrityValidationException,
)
from communs.exceptions import (
    ObjectNotFoundError as ObjectNotFoundException,
)
from communs.message_schema import MessageSchema
from database.session import get_session
from models.user import User

router = APIRouter()
user_controller = UserController()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=201, response_model=UserPublic)
async def create_new_user(user: UserSchema,
    request: Request,
    session: Session, # type: ignore  # noqa: PGH003
    )->UserPublic:
    """Create a new user."""
    new_user: User = User(**user.model_dump())
    new_user.audit_user_ip = request.client.host
    new_user.audit_user_login = 'adm'  # FIXME: Ajustar para pegar o login do usuário  # noqa: E501

    try:
        return user_controller.save(session, new_user)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object USER was not accepted',
        ) from ex


@router.get(
    '/{user_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=UserPublic,
)
def get_user_by_id(user_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    )->UserPublic:
    """Get user by id."""
    validate_transaction_access(db_session, current_user, op.OP_1040005.value)

    return user_controller.get(db_session, user_id)


@router.get('/', response_model=UserList)
def read_users(
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> UserList:
    """List all users."""
    validate_transaction_access(db_session, current_user, op.OP_1040003.value)
    users: list[User] = user_controller.get_all(db_session, skip, limit)
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_existing_user(
    user_id: int,
    user: UserSchema,
    request: Request,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
) ->UserPublic:
    """Update an existing user."""
    validate_transaction_access(db_session, current_user, op.OP_1040002.value)

    try:
        new_user: User = User(**user.model_dump())
        new_user.id = user_id

        new_user.audit_user_ip = request.client.host
        new_user.audit_user_login = (
            'adm'  # FIXME: Ajustar para pegar o login do usuário
        )

        return user_controller.update(db_session, new_user)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


@router.delete('/{user_id}', response_model=MessageSchema)
def delete_existing_user(
    user_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
) ->MessageSchema:
    """Delete an existing user."""
    validate_transaction_access(db_session, current_user, op.OP_1040004.value)

    try:
        user_controller.delete(db_session, user_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex

    return {'detail': 'User deleted'}


@router.get('/{user_id}/transactions', response_model=TransactionListSchema)
def get_user_transactions(
    user_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    ) ->TransactionListSchema:
    """Get user transactions."""
    validate_transaction_access(db_session, current_user, op.OP_1040006.value)
    return {
        'transactions': get_user_authorized_transactions(db_session, user_id),
    }
