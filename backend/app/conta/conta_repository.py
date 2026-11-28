"""Operações de persistência das contas."""

import sqlite3

from app.conta.conta_model import (
    Conta,
    ContaNaoEncontradaError,
    EmailJaCadastradoError,
)


def criar_tabela_contas(conexao: sqlite3.Connection) -> None:
    """Cria a tabela de contas caso ainda não exista."""
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            papel TEXT NOT NULL DEFAULT 'usuario',
            restrita INTEGER NOT NULL DEFAULT 0
        )
        """
    )


def _para_conta(registro: sqlite3.Row) -> Conta:
    """Converte uma linha da tabela contas em um objeto Conta."""

    return Conta(
        id=registro["id"],
        nome=registro["nome"],
        email=registro["email"],
        senha_hash=registro["senha_hash"],
        papel=registro["papel"],
        restrita=bool(registro["restrita"]),
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
        SELECT id, nome, email, senha_hash, papel, restrita
        FROM contas
        WHERE email = ?
        """,
        (email,),
    ).fetchone()

    if registro is None:
        return None

    return _para_conta(registro)


def remover_conta(conexao: sqlite3.Connection, conta_id: int) -> None:
    """Remove uma conta do banco de dados."""

    conexao.execute("DELETE FROM contas WHERE id = ?", (conta_id,))
    conexao.commit()


def buscar_conta_por_id(conexao: sqlite3.Connection, conta_id: int) -> Conta | None:
    """Busca uma conta pelo identificador."""

    registro = conexao.execute(
        "SELECT id, nome, email, senha_hash, papel, restrita FROM contas WHERE id = ?",
        (conta_id,),
    ).fetchone()

    if registro is None:
        return None

    return _para_conta(registro)


def alterar_conta(
    conexao: sqlite3.Connection,
    conta_id: int,
    nome: str,
    email: str,
    senha_hash: str,
) -> Conta:
    """Atualiza nome, e-mail e hash da senha de uma conta."""

    conexao.execute(
        "UPDATE contas SET nome = ?, email = ?, senha_hash = ? WHERE id = ?",
        (nome, email, senha_hash, conta_id),
    )
    conexao.commit()

    conta = buscar_conta_por_id(conexao, conta_id)
    assert conta is not None

    return conta


def alterar_papel(conexao: sqlite3.Connection, email: str, papel: str) -> None:
    """Atualiza o papel da conta que possui o e-mail informado."""

    cursor = conexao.execute(
        "UPDATE contas SET papel = ? WHERE email = ?",
        (papel, email),
    )
    conexao.commit()

    if cursor.rowcount == 0:
        raise ContaNaoEncontradaError("Conta não encontrada.")


def alterar_restricao(
    conexao: sqlite3.Connection,
    conta_id: int,
    restrita: bool,
) -> Conta:
    """Marca ou desmarca a conta como restrita e devolve o registro atualizado."""

    conexao.execute(
        "UPDATE contas SET restrita = ? WHERE id = ?",
        (int(restrita), conta_id),
    )
    conexao.commit()

    conta = buscar_conta_por_id(conexao, conta_id)
    assert conta is not None

    return conta
