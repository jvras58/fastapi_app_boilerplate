"""Suite de testes para main.py."""

from fastapi import status
from fastapi.testclient import TestClient
from src.main import app


def test_get_root_wellcome_msg() -> None:
    """Teste do GET /."""
    client = TestClient(app)

    respose = client.get('/')
    assert respose.status_code == status.HTTP_200_OK
    assert respose.json() == {'msg': 'Bem Vindo ao ROOT da API'}
