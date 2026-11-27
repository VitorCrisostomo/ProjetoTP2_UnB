"""Operações de persistência das contas."""

import sqlite3

from app.conta.conta_model import Conta, EmailJaCadastradoError


def criar_tabela_contas(conexao: sqlite3.Connection) -> None:
    """Cria a tabela de contas caso ainda não exista."""
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
        """
    )


def inserir_conta(
    conexao: sqlite3.Connection,
    nome: str,
    email: str,
    senha_hash: str,
) -> Conta:
    """Insere uma conta no banco de dados."""
    cursor = conexao.execute(
        """
        INSERT INTO contas (nome, email, senha_hash)
        VALUES (?, ?, ?)
        ON CONFLICT(email) DO NOTHING
        """,
        (nome, email, senha_hash),
    )

    conexao.commit()

    if cursor.rowcount == 0:
        raise EmailJaCadastradoError("E-mail já cadastrado.")

    assert cursor.lastrowid is not None

    return Conta(
        id=cursor.lastrowid,
        nome=nome,
        email=email,
        senha_hash=senha_hash,
    )


def buscar_conta_por_email(
    conexao: sqlite3.Connection,
    email: str,
) -> Conta | None:
    """Busca uma conta pelo e-mail cadastrado."""

    registro = conexao.execute(
        """
        SELECT id, nome, email, senha_hash
        FROM contas
        WHERE email = ?
        """,
        (email,),
    ).fetchone()

    if registro is None:
        return None

    return Conta(
        id=registro["id"],
        nome=registro["nome"],
        email=registro["email"],
        senha_hash=registro["senha_hash"],
    )


def remover_conta(conexao: sqlite3.Connection, conta_id: int) -> None:
    """Remove uma conta do banco de dados."""

    conexao.execute("DELETE FROM contas WHERE id = ?", (conta_id,))
    conexao.commit()
