"""Router for Authorization API."""


from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS  # noqa: N812
from sqlalchemy.orm import Session

from api.authentication.controller import get_current_user
from api.authorization.controller import validate_transaction_access
from api.authorization.schemas import (
    AuthorizationDTOSchema,
    AuthorizationListSchema,
    AuthorizationSchema,
)
from api.transaction.enum_operation_code import (
    EnumOperationCode as op,  # noqa: N813
)
from communs.exceptions import (
    IntegrityValidationError as IntegrityValidationException,
)
from communs.exceptions import (
    ObjectNotFoundError as ObjectNotFoundException,
)
from communs.generic_controller import GenericController
from communs.message_schema import MessageSchema
from database.session import get_session
from models.authorization import Authorization
from models.user import User

router = APIRouter()
controller = GenericController(Authorization)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTP_STATUS.HTTP_201_CREATED,
    response_model=AuthorizationSchema,
)
def create_authorization(
    authorization: AuthorizationDTOSchema,
    db_session: Session,  # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    request: Request,
) -> Authorization:
    """Create a new authorization."""
    validate_transaction_access(db_session, current_user, op.OP_1020001.value)
    new_authorization = Authorization(**authorization.model_dump())

    new_authorization.audit_user_ip = request.client.host
    new_authorization.audit_user_login = current_user.username

    try:
        new_authorization = controller.save(db_session, new_authorization)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object AUTHORIZATION was not accepted',
        ) from ex

    return new_authorization


@router.get(
    '/',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AuthorizationListSchema,
)
def get_all_authorizations(
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> dict[str, list[AuthorizationSchema]]:  # noqa: FA102
    """Get all authorizations."""
    validate_transaction_access(db_session, current_user, op.OP_1020003.value)
    authorizations = controller.get_all(db_session, skip, limit)
    return {'authorizations': authorizations}


@router.get(
    '/{autorization_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AuthorizationSchema,
)
def get_authorization_by_id(
    autorization_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
)-> Authorization:
    """Get an authorization by ID."""
    validate_transaction_access(db_session, current_user, op.OP_1020005.value)

    try:
        authorization = controller.get(db_session, autorization_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND,
            detail='Object AUTHORIZATION was not found',
        ) from ex

    return authorization


@router.delete(
    '/{autorization_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=MessageSchema,
)
def delete_authorization(
    autorization_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
)-> dict[str, str]:  # noqa: FA102
    """Delete an authorization."""
    validate_transaction_access(db_session, current_user, op.OP_1020004.value)

    try:
        controller.delete(db_session, autorization_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND,
            detail='Object AUTHORIZATION was not found',
        ) from ex

    return {'detail': 'Object AUTHORIZATION was deleted'}


@router.put(
    '/{autorization_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AuthorizationSchema,
)
def update_authorization(
    autorization_id: int,
    authorization: AuthorizationDTOSchema,
    db_session: Session, # type: ignore  # noqa: PGH003
    request: Request,
    current_user: CurrentUser,
)-> Authorization:
    """Update an authorization."""
    validate_transaction_access(db_session, current_user, op.OP_1020002.value)

    new_authorization: Authorization = (
        Authorization(**authorization.model_dump())
    )
    new_authorization.id = autorization_id
    new_authorization.audit_user_ip = request.client.host
    new_authorization.audit_user_login = current_user.username

    try:
        return controller.update(db_session, new_authorization)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0],
        ) from ex
