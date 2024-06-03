"""Exceptions."""
from fastapi import HTTPException, status


class CredentialsValidationException(HTTPException):
    """Representa um erro de validação de credencial do usuário."""

    def __init__(self) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class IncorrectCredentialError(Exception):
    """Representao o erro de Login e Senha inválidos."""

    def __init__(self) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__('Incorrect email or password')


class ObjectAlreadyError(Exception):
    """Representao o erro quando se tentar cadastrar um usuário com o mesmo username."""  # noqa: E501

    def __init__(self, obj_type: str, obj_id: str) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(f'Object {obj_type} already exist with id [{obj_id}]')


class ObjectNotFoundError(Exception):
    """Representa um erro quando o usuário com determinado ID não é encontrado."""  # noqa: E501

    def __init__(self, obj_type: str, obj_id: str) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(f'{obj_type} with ID [{obj_id}] not found')


class ValueRequiredError(Exception):
    """Representa um erro é detectada a ausencia de um valor obrigatório."""

    def __init__(self, field_name: str) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(f'{field_name} cannot be null')


class IntegrityValidationError(Exception):
    """Representa um erro de validação de integridade de dados."""

    def __init__(self, exc_msg: str) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(exc_msg)


class IllegalAccessExcetion(HTTPException):
    """Representa um erro de acesso ilegal."""

    def __init__(self, user_id: int, op_code: str) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                f'User[{user_id}] not authorized to access '
                f'Transaction[{op_code}]'
            ),
            headers={'WWW-Authenticate': 'Bearer'},
        )


class AmbiguousAuthorizationException(HTTPException):
    """Representa um erro de definição ambigoa de autorização."""

    def __init__(self, user_id: int, op_code: str) -> None:
        """Inicializa uma nova instância da classe."""
        msg = (
            f'Found more than one authorization for User[{user_id}] '
            f'and Transaction[{op_code}]'
        )
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg,
            headers={'WWW-Authenticate': 'Bearer'},
        )


class ObjectConflitError(Exception):
    """Representa um erro quando um objeto entra em conflito com outro."""

    def __init__(self, obj_type: str, obj_id: str) -> None:
        """Inicializa uma nova instância da classe."""
        super().__init__(f'{obj_type} with ID [{obj_id}] conflict availability')
