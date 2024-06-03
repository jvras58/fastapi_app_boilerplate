"""teste."""
from datetime import datetime, timedelta

from bcrypt import checkpw, gensalt, hashpw
from jose import jwt

from config.settings import get_settings


def create_access_token(data: dict) -> str:
    """"Acess token."""
    to_encode = data.copy()
    current_time = datetime.datetime.utcnow()
    expire = current_time + timedelta(
        minutes=get_settings().SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    to_encode.update({'exp': expire})
    to_encode.update({'nbf': current_time})
    to_encode.update({'iat': current_time})
    to_encode.update({'iss': 'FP-Backend'})

    return jwt.encode(
        to_encode,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithm=get_settings().SECURITY_ALGORITHM,
    )



def get_password_hash(password: str) -> bytes:
    """Get password hash."""
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    plain_password_encoded = plain_password.encode('utf-8')

    # Esta converção é necessária para que o bcrypt consiga comparar
    # as senhas quando a string vem do BD.
    if isinstance(hashed_password, str):
        hashed_password = bytes(hashed_password, 'utf-8')

    return checkpw(plain_password_encoded, hashed_password)


def extract_username(jwt_token: str) -> str:
    """Extract username from jwt token."""
    payload = jwt.decode(
        jwt_token,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithms=[get_settings().SECURITY_ALGORITHM],
    )
    return payload.get('sub')
