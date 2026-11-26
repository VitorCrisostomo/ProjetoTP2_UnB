"""Testes dos endpoints de gerenciamento de contas."""

from pathlib import Path

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
