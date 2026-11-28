"""Regras de negócio dos tipos de ocorrência."""

from app.conta.conta_model import DadosInvalidosError


def validar_nome_tipo(nome: object) -> str:
    """Exige um nome preenchido e o devolve sem espaços nas pontas."""

    if not isinstance(nome, str) or not nome.strip():
        raise DadosInvalidosError("Nome inválido.")

    return nome.strip()
