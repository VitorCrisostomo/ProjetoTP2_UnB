"""Regras de negócio dos tipos de ocorrência."""

import sqlite3

from app.conta.conta_model import DadosInvalidosError
from app.tipo.tipo_model import TipoJaExisteError, TipoOcorrencia
from app.tipo.tipo_repository import buscar_tipo_por_nome, inserir_tipo


def validar_nome_tipo(nome: object) -> str:
    """Exige um nome preenchido e o devolve sem espaços nas pontas."""

    if not isinstance(nome, str) or not nome.strip():
        raise DadosInvalidosError("Nome inválido.")

    return nome.strip()


def criar_tipo(conexao: sqlite3.Connection, nome: object) -> TipoOcorrencia:
    """Valida o nome e cadastra um novo tipo de ocorrência."""

    nome_validado = validar_nome_tipo(nome)

    if buscar_tipo_por_nome(conexao, nome_validado) is not None:
        raise TipoJaExisteError("Tipo já existe.")

    return inserir_tipo(conexao, nome_validado)
