"""Router for Assignment API."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS  # noqa: N812
from sqlalchemy.orm import Session

from api.assignment.schemas import (
    AssignmentDTOSchema,
    AssignmentListSchema,
    AssignmentSchema,
)
from api.authentication.controller import get_current_user
from api.authorization.controller import validate_transaction_access
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
from models.assignment import Assignment
from models.user import User

router = APIRouter()
controller = GenericController(Assignment)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AssignmentSchema,
)
def get_assignment_by_id(
    assignment_id: int, db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
)-> AssignmentSchema:
    """Get an assignment by ID."""
    validate_transaction_access(db_session, current_user, op.OP_1010005.value)

    return controller.get(db_session, assignment_id)


@router.get(
    '/', status_code=HTTP_STATUS.HTTP_200_OK, response_model=AssignmentListSchema,  # noqa: E501
)
def get_all_assignments(
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> AssignmentListSchema:
    """Get all assignments."""
    validate_transaction_access(db_session, current_user, op.OP_1010003.value)
    assignments = controller.get_all(db_session, skip, limit)
    return {'assignments': assignments}


@router.post(
    '/', status_code=HTTP_STATUS.HTTP_201_CREATED, response_model=AssignmentSchema,  # noqa: E501
)
def create_assignment(
    assignment: AssignmentDTOSchema,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    request: Request,
)-> AssignmentSchema:
    """Create an assignment."""
    validate_transaction_access(db_session, current_user, op.OP_1010001.value)

    new_assignment = Assignment(**assignment.model_dump())
    new_assignment.audit_user_ip = request.client.host
    new_assignment.audit_user_login = current_user.username

    try:
        new_assignment = controller.save(db_session, new_assignment)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object ASSIGNMENT was not accepted',
        ) from ex

    return new_assignment


@router.put(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AssignmentSchema,
)
def update_assignment(
    assignment_id: int,
    assignment: AssignmentDTOSchema,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
    request: Request,
) -> AssignmentSchema:
    """Update an assignment."""
    validate_transaction_access(db_session, current_user, op.OP_1010002.value)

    new_assignment: Assignment = Assignment(**assignment.model_dump())
    new_assignment.id = assignment_id
    new_assignment.audit_user_ip = request.client.host
    new_assignment.audit_user_login = current_user.username

    try:
        new_assignment = controller.update(db_session, new_assignment)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object ASSIGNMENT was not accepted',
        ) from ex

    return new_assignment


@router.delete(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=MessageSchema,
)
def delete_assignment(
    assignment_id: int,
    db_session: Session, # type: ignore  # noqa: PGH003
    current_user: CurrentUser,
) -> MessageSchema:
    """Delete an assignment."""
    validate_transaction_access(db_session, current_user, op.OP_1010004.value)

    try:
        controller.delete(db_session, assignment_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0],
        ) from ex

    return {'detail': 'Assignment deleted successfully'}
