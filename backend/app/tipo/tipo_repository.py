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


def listar_tipos_ativos(conexao: sqlite3.Connection) -> list[TipoOcorrencia]:
    """Lista os tipos de ocorrência ativos, do mais antigo ao mais recente."""

    registros = conexao.execute(
        "SELECT id, nome, ativo FROM tipos_ocorrencia WHERE ativo = 1 ORDER BY id"
    ).fetchall()

    return [_para_tipo(registro) for registro in registros]


def buscar_tipo_por_id(
    conexao: sqlite3.Connection,
    tipo_id: int,
) -> TipoOcorrencia | None:
    """Busca um tipo de ocorrência pelo identificador."""

    registro = conexao.execute(
        "SELECT id, nome, ativo FROM tipos_ocorrencia WHERE id = ?",
        (tipo_id,),
    ).fetchone()

    if registro is None:
        return None

    return _para_tipo(registro)


def alterar_nome_tipo(
    conexao: sqlite3.Connection,
    tipo_id: int,
    nome: str,
) -> TipoOcorrencia:
    """Altera o nome de um tipo de ocorrência e devolve o registro atualizado."""

    conexao.execute(
        "UPDATE tipos_ocorrencia SET nome = ? WHERE id = ?",
        (nome, tipo_id),
    )
    conexao.commit()

    tipo = buscar_tipo_por_id(conexao, tipo_id)
    assert tipo is not None

    return tipo
