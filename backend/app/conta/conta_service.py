"""Regras de negócio relacionadas às contas."""

import re
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from app.conta.conta_model import Conta, DadosInvalidosError
from app.conta.conta_repository import (
    buscar_conta_por_email,
    buscar_conta_por_id,
    inserir_conta,
    remover_conta,
)


def validar_senha(senha: str) -> None:
    """Exige ao menos 8 caracteres, com pelo menos uma letra e um número."""

    if (
        len(senha) < 8
        or not any(c.isdigit() for c in senha)
        or not any(c.isalpha() for c in senha)
    ):
        raise DadosInvalidosError("Senha inválida.")


def validar_dados(
    nome: object,
    email: object,
    senha: object,
) -> tuple[str, str, str]:
    """Valida os dados fornecidos para uma conta."""

    if (
        not isinstance(nome, str)
        or not isinstance(email, str)
        or not isinstance(senha, str)
        or not nome.strip()
        or not email.strip()
        or not senha.strip()
    ):
        raise DadosInvalidosError("Campos obrigatórios.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise DadosInvalidosError("E-mail inválido.")

    validar_senha(senha)

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


def autenticar_conta(
    conexao: sqlite3.Connection,
    email: object,
    senha: object,
) -> Conta | None:
    """Autentica uma conta utilizando e-mail e senha."""

    if (
        not isinstance(email, str)
        or not isinstance(senha, str)
        or not email.strip()
        or not senha.strip()
    ):
        raise DadosInvalidosError("Campos obrigatórios.")

    conta = buscar_conta_por_email(conexao, email)

    if conta is None:
        return None

    if not check_password_hash(conta.senha_hash, senha):
        return None

    return conta


def excluir_conta(conexao: sqlite3.Connection, conta_id: int) -> None:
    """Exclui a conta com o identificador informado."""

    remover_conta(conexao, conta_id)


def obter_conta(conexao: sqlite3.Connection, conta_id: int) -> Conta | None:
    """Busca uma conta pelo identificador."""

    return buscar_conta_por_id(conexao, conta_id)


def atualizar_conta(
    conexao: sqlite3.Connection,
    conta: Conta,
    nome: object,
    email: object,
    senha: object,
) -> Conta:
    """Valida e atualiza os dados da conta do usuário."""

    if (
        not isinstance(nome, str)
        or not isinstance(email, str)
        or not nome.strip()
        or not email.strip()
    ):
        raise DadosInvalidosError("Campos obrigatórios.")

    return conta
