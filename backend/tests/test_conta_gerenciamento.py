"""Testes de exclusão e edição da própria conta."""

from flask import Flask
from flask.testing import FlaskClient

from app.db import get_db


def test_excluir_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU03 C1: usuário não autenticado não pode excluir conta."""
    response = client.delete("/conta")

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_excluir_conta_sem_confirmacao_mantem_a_conta(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU03 C2: sem confirmação, a conta não é excluída."""
    response = client.delete("/conta")

    assert response.status_code == 200
    assert response.get_json() == {"excluida": False}
    login = client.post(
        "/login",
        json={"email": conta_logada["email"], "senha": conta_logada["senha"]},
    )
    assert login.status_code == 200


def test_excluir_conta_confirmada_remove_a_conta(
    app: Flask,
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU03 C3: com confirmação, a conta é removida do banco."""
    response = client.delete("/conta", json={"confirmar": True})

    assert response.status_code == 204
    with app.app_context():
        total = get_db().execute("SELECT COUNT(*) FROM contas").fetchone()[0]
    assert total == 0
