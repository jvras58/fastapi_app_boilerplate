"""Define the routes for the role module."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS  # noqa: N812
from sqlalchemy.orm import Session

from api.authentication.controller import get_current_user
from api.authorization.controller import validate_transaction_access
from api.role.schemas import RoleDTOSchema, RoleListSchema, RoleSchema
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
from models.role import Role
from models.user import User

router = APIRouter()
role_controller = GenericController(Role)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/{role_id}', status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=RoleSchema,
)
def get_role_by_id(role_id: int,
     db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
) -> RoleSchema:
    """Get a role by its id."""
    validate_transaction_access(db_session, current_user, op.OP_1050005.value)

    return role_controller.get(db_session, role_id)


@router.get('/', status_code=HTTP_STATUS.HTTP_200_OK, response_model=RoleListSchema,  # noqa: E501
)
def get_all_roles(
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> RoleListSchema:
    """Get all roles."""
    validate_transaction_access(db_session, current_user, op.OP_1050003.value)
    roles = role_controller.get_all(db_session, skip, limit)
    return {'roles': roles}


@router.post('/', status_code=HTTP_STATUS.HTTP_201_CREATED,response_model=RoleSchema, # noqa: E501
)
def create_role(
    role: RoleDTOSchema,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    request: Request,
)-> RoleSchema:
    """Create a new role."""
    validate_transaction_access(db_session, current_user, op.OP_1050001.value)
    new_role = Role(**role.model_dump())

    new_role.audit_user_ip = request.client.host
    new_role.audit_user_login = current_user.username

    try:
        new_role = role_controller.save(db_session, new_role)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object ROLE was not accepted',
        ) from ex

    return new_role


@router.put(
    '/{role_id}', status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=RoleSchema,
)
def update_role(
    role_id: int,
    role: RoleDTOSchema,
    db_session: Session, # type: ignore  # noqa: PGH003
    request: Request,
    current_user: CurrentUser,
) -> RoleSchema:
    """Update a role."""
    validate_transaction_access(db_session, current_user, op.OP_1050002.value)

    new_role: Role = Role(**role.model_dump())
    new_role.id = role_id
    new_role.audit_user_ip = request.client.host
    new_role.audit_user_login = current_user.username

    try:
        return role_controller.update(db_session, new_role)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0],
        ) from ex


@router.delete(
    '/{role_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=MessageSchema,
)
def delete_role(
    role_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
) -> MessageSchema:
    """Delete a role."""
    validate_transaction_access(db_session, current_user, op.OP_1050004.value)

    try:
        role_controller.delete(db_session, role_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND,
            detail=ex.args[0],
        ) from ex

    return {'detail': 'Role deleted successfully'}
