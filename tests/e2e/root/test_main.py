"""Suite de testes para main.py."""

from fastapi import status
from fastapi.testclient import TestClient
from src.main import app


def test_get_root_wellcome_msg_success() -> None:
    """Teste do GET /."""
    # Quando a rota GET / é chamada
    client = TestClient(app)

    respose = client.get('/')

    # Entáo a API deve responder com status 200 OK
    assert respose.status_code == status.HTTP_200_OK

    # E o corpo da resposta deve conter a mensagem informando que a API está
    # rodando
    assert 'id' in respose.json()
    assert 'type' in respose.json()
    assert 'sumary' in respose.json()
    assert 'message' in respose.json()
    assert respose.json()['id'] == 1
    assert respose.json()['type'] == 'success'
    assert respose.json()['sumary'] == 'API is running'
    assert respose.json()['message'] == 'API is running'
