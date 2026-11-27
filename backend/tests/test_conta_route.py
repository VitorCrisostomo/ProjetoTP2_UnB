"""Testes dos endpoints de gerenciamento de contas."""

from pathlib import Path

import pytest
from flask.testing import FlaskClient
from werkzeug.security import check_password_hash

from app import create_app
from app.db import get_db, init_db


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


def test_cadastrar_conta_sem_json(tmp_path: Path) -> None:
    """Verifica a rejeição de uma requisição sem JSON."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
        }
    )

    with app.app_context():
        init_db()

    client = app.test_client()

    response = client.post("/contas")

    assert response.status_code == 400
    assert "erro" in response.get_json()


def test_persistencia_conta_e_hash(tmp_path: Path) -> None:
    """Verifica a persistência e o armazenamento seguro da senha."""
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

    with app.app_context():
        conta = (
            get_db()
            .execute(
                "SELECT * FROM contas WHERE email = ?",
                ("usuario@teste.com",),
            )
            .fetchone()
        )

        assert conta is not None
        assert conta["id"] == response.get_json()["id"]
        assert conta["nome"] == "Usuario Teste"
        assert conta["senha_hash"] != "Senha123"
        assert check_password_hash(conta["senha_hash"], "Senha123")


def test_login_credenciais_validas(tmp_path: Path) -> None:
    """Verifica a autenticação com credenciais válidas."""
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "SECRET_KEY": "chave-exclusiva-de-teste",
        }
    )

    with app.app_context():
        init_db()

    client = app.test_client()

    cadastro = client.post(
        "/contas",
        json={
            "nome": "Usuario Teste",
            "email": "usuario@teste.com",
            "senha": "Senha123",
        },
    )

    assert cadastro.status_code == 201

    response = client.post(
        "/login",
        json={
            "email": "usuario@teste.com",
            "senha": "Senha123",
        },
    )

    assert response.status_code == 200

    with client.session_transaction() as sessao:
        assert sessao["conta_id"] == cadastro.get_json()["id"]


def test_login_sem_senha_informa_campos_obrigatorios(client: FlaskClient) -> None:
    """HU01 C1: campo ausente no login retorna erro de campos obrigatórios."""
    response = client.post("/login", json={"email": "usuario@teste.com"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios."}


def test_login_sem_email_informa_campos_obrigatorios(client: FlaskClient) -> None:
    """HU01 C1: e-mail ausente no login retorna erro de campos obrigatórios."""
    response = client.post("/login", json={"senha": "Senha123"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios."}


def test_login_com_senha_errada_retorna_credenciais_invalidas(
    client: FlaskClient,
    conta_cadastrada: dict[str, str],
) -> None:
    """HU01: senha incorreta não autentica nem cria sessão."""
    response = client.post(
        "/login",
        json={"email": conta_cadastrada["email"], "senha": "SenhaErrada1"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Credenciais inválidas."}
    with client.session_transaction() as sessao:
        assert "conta_id" not in sessao


def test_login_com_email_nao_cadastrado_retorna_credenciais_invalidas(
    client: FlaskClient,
) -> None:
    """HU01: e-mail inexistente retorna a mesma mensagem de senha errada."""
    response = client.post(
        "/login",
        json={"email": "naoexiste@teste.com", "senha": "Senha123"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Credenciais inválidas."}


def test_login_com_email_mal_formatado_retorna_credenciais_invalidas(
    client: FlaskClient,
) -> None:
    """HU01: e-mail sem formato válido não está cadastrado, logo é 401."""
    response = client.post(
        "/login",
        json={"email": "emailinvalido", "senha": "Senha123"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Credenciais inválidas."}


def test_login_sem_corpo_json_retorna_400(client: FlaskClient) -> None:
    """HU01: requisição sem JSON válido é recusada."""
    response = client.post("/login", data="texto puro")

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Dados inválidos."}


def test_cadastro_sem_senha_informa_campos_obrigatorios(client: FlaskClient) -> None:
    """HU02 C1: campo ausente retorna erro de campos obrigatórios."""
    response = client.post(
        "/contas",
        json={"nome": "Usuario", "email": "usuario@teste.com"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios."}


def test_cadastro_com_senha_curta_e_rejeitado(client: FlaskClient) -> None:
    """HU02 C3: senha com menos de 8 caracteres é inválida."""
    response = client.post(
        "/contas",
        json={"nome": "Usuario", "email": "usuario@teste.com", "senha": "Ab1"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Senha inválida."}


def test_cadastro_senha_sem_numero_e_rejeitada(client: FlaskClient) -> None:
    """HU02 C3: senha sem nenhum número é inválida."""
    response = client.post(
        "/contas",
        json={
            "nome": "Usuario",
            "email": "usuario@teste.com",
            "senha": "SomenteLetras",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Senha inválida."}


def test_cadastro_senha_sem_letra_e_rejeitada(client: FlaskClient) -> None:
    """HU02 C3: senha sem nenhuma letra é inválida."""
    response = client.post(
        "/contas",
        json={
            "nome": "Usuario",
            "email": "usuario@teste.com",
            "senha": "12345678",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Senha inválida."}
