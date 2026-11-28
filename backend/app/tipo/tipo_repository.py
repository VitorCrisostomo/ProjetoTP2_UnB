"""Operações de persistência dos tipos de ocorrência."""

import sqlite3

from app.tipo.tipo_model import TipoOcorrencia


def criar_tabela_tipos(conexao: sqlite3.Connection) -> None:
    """Cria a tabela de tipos de ocorrência, caso ela ainda não exista."""

    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS tipos_ocorrencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            ativo INTEGER NOT NULL DEFAULT 1
        )
        """
    )
    conexao.commit()


def inserir_tipo(conexao: sqlite3.Connection, nome: str) -> TipoOcorrencia:
    """Insere um novo tipo de ocorrência ativo."""

    cursor = conexao.execute(
        "INSERT INTO tipos_ocorrencia (nome) VALUES (?)",
        (nome,),
    )
    conexao.commit()

    assert cursor.lastrowid is not None

    return TipoOcorrencia(id=cursor.lastrowid, nome=nome, ativo=True)


def _para_tipo(registro: sqlite3.Row) -> TipoOcorrencia:
    """Converte uma linha da tabela de tipos em um objeto TipoOcorrencia."""

    return TipoOcorrencia(
        id=registro["id"],
        nome=registro["nome"],
        ativo=bool(registro["ativo"]),
    )


def buscar_tipo_por_nome(
    conexao: sqlite3.Connection,
    nome: str,
) -> TipoOcorrencia | None:
    """Busca um tipo de ocorrência pelo nome."""

    registro = conexao.execute(
        "SELECT id, nome, ativo FROM tipos_ocorrencia WHERE nome = ?",
        (nome,),
    ).fetchone()

    if registro is None:
        return None

    return _para_tipo(registro)
