"""Fixtures compartilhadas pelos testes."""

from collections.abc import Callable
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.conta.conta_service import definir_papel
from app.db import get_db, init_db


@pytest.fixture
def app(tmp_path: Path) -> Flask:
    """Cria uma aplicação com banco SQLite temporário e vazio."""
    aplicacao = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "SECRET_KEY": "chave-exclusiva-de-teste",
        }
    )
    with aplicacao.app_context():
        init_db()
    return aplicacao


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Cliente HTTP de teste ligado ao banco temporário."""
    return app.test_client()


@pytest.fixture
def conta_cadastrada(client: FlaskClient) -> dict[str, str]:
    """Cadastra uma conta comum e devolve seus dados em texto puro."""
    dados = {
        "nome": "Usuario Teste",
        "email": "usuario@teste.com",
        "senha": "Senha123",
    }
    assert client.post("/contas", json=dados).status_code == 201
    return dados


@pytest.fixture
def conta_logada(
    client: FlaskClient,
    conta_cadastrada: dict[str, str],
) -> dict[str, str]:
    """Cadastra uma conta e autentica o cliente de teste com ela."""
    resposta = client.post(
        "/login",
        json={
            "email": conta_cadastrada["email"],
            "senha": conta_cadastrada["senha"],
        },
    )
    assert resposta.status_code == 200
    return conta_cadastrada


@pytest.fixture
def logar_como(app: Flask) -> Callable[[str], FlaskClient]:
    """Devolve uma função que cria um cliente autenticado com o papel pedido."""

    def _logar(papel: str) -> FlaskClient:
        cliente = app.test_client()
        email = f"{papel}@papel.teste.com"
        dados = {"nome": f"Conta {papel}", "email": email, "senha": "Senha123"}
        assert cliente.post("/contas", json=dados).status_code == 201
        with app.app_context():
            definir_papel(get_db(), email, papel)
        resposta = cliente.post("/login", json={"email": email, "senha": "Senha123"})
        assert resposta.status_code == 200
        return cliente

    return _logar


@pytest.fixture
def conta_alvo(client: FlaskClient) -> int:
    """Cadastra uma conta comum e devolve o seu identificador."""
    resposta = client.post(
        "/contas",
        json={"nome": "Conta Alvo", "email": "alvo@teste.com", "senha": "Senha123"},
    )
    assert resposta.status_code == 201
    return int(resposta.get_json()["id"])


@pytest.fixture
def usuario(logar_como: Callable[[str], FlaskClient]) -> FlaskClient:
    """Cliente autenticado como usuário comum."""
    return logar_como("usuario")


@pytest.fixture
def administrador(logar_como: Callable[[str], FlaskClient]) -> FlaskClient:
    """Cliente autenticado como administrador."""
    return logar_como("administrador")
