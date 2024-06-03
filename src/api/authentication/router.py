"""Authentication router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.authentication.controller import execute_user_login
from api.authentication.schemas import AccessToken
from communs.exceptions import IncorrectCredentialError
from database.session import Session, get_session

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=AccessToken)
def login_for_access_token(
    form_data: OAuth2Form,
    db_session: Session,  # type: ignore  # noqa: PGH003
) -> AccessToken:
    """Login for access token."""
    try:
        return execute_user_login(
            db_session,
            form_data.username,
            form_data.password,
        )
    except IncorrectCredentialError as ex:
        raise HTTPException(status_code=400, detail=ex.args[0]) from ex
