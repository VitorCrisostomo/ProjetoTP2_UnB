"""Testes dos papéis de conta (usuário, moderador, administrador)."""

from flask import Flask
from flask.testing import FlaskClient


def test_definir_papel_promove_conta_existente(
    app: Flask,
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """O comando definir-papel altera o papel da conta pelo e-mail."""
    runner = app.test_cli_runner()
    email = conta_logada["email"]

    resultado = runner.invoke(args=["definir-papel", email, "moderador"])

    assert resultado.exit_code == 0
    assert client.get("/conta").get_json()["papel"] == "moderador"


def test_definir_papel_invalido_e_recusado(
    app: Flask,
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """Papéis fora de usuario, moderador e administrador não são aceitos."""
    runner = app.test_cli_runner()
    email = conta_logada["email"]

    resultado = runner.invoke(args=["definir-papel", email, "chefe"])

    assert resultado.exit_code != 0
    assert "Papel inválido." in resultado.output
    assert client.get("/conta").get_json()["papel"] == "usuario"


def test_definir_papel_de_conta_inexistente_e_recusado(app: Flask) -> None:
    """O comando informa erro quando não há conta com o e-mail."""
    runner = app.test_cli_runner()
    email = "ninguem@teste.com"

    resultado = runner.invoke(args=["definir-papel", email, "moderador"])

    assert resultado.exit_code != 0
    assert "Conta não encontrada." in resultado.output
