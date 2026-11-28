"""Testes dos papéis de conta (usuário e administrador)."""

from collections.abc import Callable

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

    resultado = runner.invoke(args=["definir-papel", email, "administrador"])

    assert resultado.exit_code == 0
    assert client.get("/conta").get_json()["papel"] == "administrador"


def test_definir_papel_invalido_e_recusado(
    app: Flask,
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """Papéis fora de usuario e administrador não são aceitos."""
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

    resultado = runner.invoke(args=["definir-papel", email, "administrador"])

    assert resultado.exit_code != 0
    assert "Conta não encontrada." in resultado.output


def test_editar_conta_devolve_o_papel_da_conta(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """A edição de dados não altera nem esconde o papel da conta."""
    administrador = logar_como("administrador")

    response = administrador.put(
        "/conta",
        json={
            "nome": "Administrador Novo",
            "email": "administrador@papel.teste.com",
            "confirmar": True,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["papel"] == "administrador"


def test_login_devolve_o_papel_da_conta(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """O login informa o papel gravado no banco, não um valor padrão."""
    administrador = logar_como("administrador")

    response = administrador.post(
        "/login",
        json={"email": "administrador@papel.teste.com", "senha": "Senha123"},
    )

    assert response.status_code == 200
    assert response.get_json()["papel"] == "administrador"
