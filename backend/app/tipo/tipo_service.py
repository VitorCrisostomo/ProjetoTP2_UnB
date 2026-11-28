"""Regras de negócio dos tipos de ocorrência."""

import sqlite3

from app.conta.conta_model import DadosInvalidosError
from app.tipo.tipo_model import TipoOcorrencia
from app.tipo.tipo_repository import inserir_tipo


def validar_nome_tipo(nome: object) -> str:
    """Exige um nome preenchido e o devolve sem espaços nas pontas."""

    if not isinstance(nome, str) or not nome.strip():
        raise DadosInvalidosError("Nome inválido.")

    return nome.strip()


def criar_tipo(conexao: sqlite3.Connection, nome: object) -> TipoOcorrencia:
    """Valida o nome e cadastra um novo tipo de ocorrência."""

    return inserir_tipo(conexao, validar_nome_tipo(nome))
