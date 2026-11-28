"""Testes da restrição de contas por moderadores (HU14)."""

from flask.testing import FlaskClient


def test_restringir_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU14 C1: usuário não autenticado não restringe contas."""
    response = client.put("/contas/1/restricao", json={"restrita": True})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}
