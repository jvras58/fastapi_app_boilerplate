"""Session."""


from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config.settings import get_settings

engine = create_engine(get_settings().DB_URL)


def get_session() -> Session: # type: ignore  # noqa: PGH003
    """Retorna uma sessão do banco de dados."""
    with Session(engine) as session:
        yield session
