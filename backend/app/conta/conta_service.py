"""Regras de negócio relacionadas às contas."""

import re
import sqlite3

from werkzeug.security import generate_password_hash

from app.conta.conta_model import Conta, DadosInvalidosError
from app.conta.conta_repository import inserir_conta


def validar_dados(
    nome: object,
    email: object,
    senha: object,
) -> tuple[str, str, str]:
    """Valida os dados fornecidos para uma conta."""

    if not isinstance(nome, str) or not nome.strip():
        raise DadosInvalidosError("Nome inválido.")

    if not isinstance(email, str) or not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
        raise DadosInvalidosError("E-mail inválido.")

    if not isinstance(senha, str) or not senha.strip():
        raise DadosInvalidosError("Senha inválida.")

    return nome, email, senha


def cadastrar_conta(
    conexao: sqlite3.Connection,
    nome: object,
    email: object,
    senha: object,
) -> Conta:
    """Valida e cadastra uma conta armazenando o hash da senha."""

    nome_validado, email_validado, senha_validada = validar_dados(nome, email, senha)

    senha_hash = generate_password_hash(senha_validada)

    return inserir_conta(
        conexao,
        nome_validado,
        email_validado,
        senha_hash,
    )
