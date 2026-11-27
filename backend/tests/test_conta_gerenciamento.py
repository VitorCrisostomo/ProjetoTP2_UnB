"""Testes de exclusão e edição da própria conta."""

from flask.testing import FlaskClient


def test_excluir_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU03 C1: usuário não autenticado não pode excluir conta."""
    response = client.delete("/conta")

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}
