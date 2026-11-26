"""Regras de negócio relacionadas às contas."""

import sqlite3

from werkzeug.security import generate_password_hash

from app.conta.conta_model import Conta
from app.conta.conta_repository import inserir_conta


def cadastrar_conta(
    conexao: sqlite3.Connection,
    nome: str,
    email: str,
    senha: str,
) -> Conta:
    """Cadastra uma conta armazenando a senha de forma segura."""
    senha_hash = generate_password_hash(senha)

    return inserir_conta(
        conexao,
        nome,
        email,
        senha_hash,
    )
