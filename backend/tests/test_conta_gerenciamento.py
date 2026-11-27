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


def test_excluir_conta_invalida_sessao_e_credenciais(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU03 C3: após excluir, a sessão e as credenciais deixam de valer."""
    client.delete("/conta", json={"confirmar": True})

    with client.session_transaction() as sessao:
        assert "conta_id" not in sessao
    login = client.post(
        "/login",
        json={"email": conta_logada["email"], "senha": conta_logada["senha"]},
    )
    assert login.status_code == 401


def test_excluir_conta_com_sessao_de_conta_inexistente_retorna_401(
    app: Flask,
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """Sessão antiga de uma conta já apagada não conta como autenticada."""
    with app.app_context():
        conexao = get_db()
        conexao.execute("DELETE FROM contas")
        conexao.commit()

    response = client.delete("/conta", json={"confirmar": True})

    assert response.status_code == 401


def test_consultar_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU04 C1: usuário não autenticado não consulta dados de conta."""
    response = client.get("/conta")

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_consultar_conta_retorna_dados_sem_senha(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU04: o usuário autenticado vê os dados atuais da própria conta."""
    response = client.get("/conta")

    assert response.status_code == 200
    dados = response.get_json()
    assert dados["nome"] == conta_logada["nome"]
    assert dados["email"] == conta_logada["email"]
    assert "senha" not in dados
    assert "senha_hash" not in dados


def test_editar_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU04 C1: usuário não autenticado não edita conta."""
    response = client.put("/conta", json={"nome": "Novo", "confirmar": True})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_editar_conta_sem_confirmacao_mantem_os_dados(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU04 C2: sem confirmação, os dados anteriores são mantidos."""
    response = client.put(
        "/conta",
        json={"nome": "Nome Novo", "email": "novo@teste.com"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"atualizada": False}
    consulta = client.get("/conta").get_json()
    assert consulta["nome"] == conta_logada["nome"]
    assert consulta["email"] == conta_logada["email"]


def test_editar_conta_com_nome_vazio_retorna_400(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU04 C3: dados inválidos são recusados e os anteriores permanecem."""
    response = client.put(
        "/conta",
        json={"nome": "", "email": conta_logada["email"], "confirmar": True},
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios."}
    assert client.get("/conta").get_json()["nome"] == conta_logada["nome"]


def test_editar_conta_com_email_invalido_retorna_400(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU04 C3: e-mail sem formato válido é recusado."""
    response = client.put(
        "/conta",
        json={"nome": "Nome Novo", "email": "emailinvalido", "confirmar": True},
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "E-mail inválido."}
    assert client.get("/conta").get_json()["email"] == conta_logada["email"]


def test_editar_conta_com_senha_fraca_retorna_400(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU04 C3: nova senha que não atende às regras é recusada."""
    response = client.put(
        "/conta",
        json={
            "nome": conta_logada["nome"],
            "email": conta_logada["email"],
            "senha": "123",
            "confirmar": True,
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Senha inválida."}
