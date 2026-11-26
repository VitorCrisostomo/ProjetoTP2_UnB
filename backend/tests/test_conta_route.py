"""Testes dos endpoints de gerenciamento de contas."""

from pathlib import Path

import pytest

from app import create_app
from app.db import init_db


def test_cadastrar_conta_valida(tmp_path: Path) -> None:
    """Verifica o cadastro de uma conta com dados válidos."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )

    with app.app_context():
        init_db()
    client = app.test_client()

    response = client.post(
        "/contas",
        json={
            "nome": "Usuario Teste",
            "email": "usuario@teste.com",
            "senha": "Senha123",
        },
    )

    assert response.status_code == 201

    dados = response.get_json()

    assert dados["nome"] == "Usuario Teste"
    assert dados["email"] == "usuario@teste.com"
    assert "id" in dados
    assert "senha" not in dados
    assert "senha_hash" not in dados


def test_cadastrar_conta_email_duplicado(tmp_path: Path) -> None:
    """Verifica se o sistema impede o cadastro de e-mails duplicados."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )

    with app.app_context():
        init_db()

    client = app.test_client()

    primeira_resposta = client.post(
        "/contas",
        json={
            "nome": "Primeiro Usuario",
            "email": "usuario@teste.com",
            "senha": "Senha123",
        },
    )

    assert primeira_resposta.status_code == 201

    segunda_resposta = client.post(
        "/contas",
        json={
            "nome": "Segundo Usuario",
            "email": "usuario@teste.com",
            "senha": "OutraSenha123",
        },
    )

    assert segunda_resposta.status_code == 409


@pytest.mark.parametrize(
    "dados_invalidos",
    [
        {"nome": "", "email": "usuario@teste.com", "senha": "Senha123"},
        {"nome": "   ", "email": "usuario@teste.com", "senha": "Senha123"},
        {"nome": "Usuario", "email": "emailinvalido", "senha": "Senha123"},
        {"nome": "Usuario", "email": "", "senha": "Senha123"},
        {"nome": "Usuario", "email": "usuario@teste.com", "senha": ""},
        {"email": "usuario@teste.com", "senha": "Senha123"},
        {"nome": "Usuario", "senha": "Senha123"},
        {"nome": "Usuario", "email": "usuario@teste.com"},
        {"nome": 123, "email": "usuario@teste.com", "senha": "Senha123"},
        {"nome": "Usuario", "email": None, "senha": "Senha123"},
        {"nome": "Usuario", "email": "usuario@teste.com", "senha": 123},
    ],
)
def test_cadastrar_conta_dados_invalidos(
    tmp_path: Path,
    dados_invalidos: dict[str, object],
) -> None:
    """Verifica a rejeição de dados inválidos no cadastro."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )

    with app.app_context():
        init_db()

    client = app.test_client()

    response = client.post("/contas", json=dados_invalidos)

    assert response.status_code == 400

    dados = response.get_json()
    assert "erro" in dados
