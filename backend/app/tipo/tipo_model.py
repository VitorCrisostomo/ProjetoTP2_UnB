"""Modelo de dados da entidade TipoOcorrencia."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TipoOcorrencia:
    """Representa um tipo de ocorrência disponível no sistema."""

    id: int
    nome: str
    ativo: bool


class TipoJaExisteError(Exception):
    """Indica que já existe um tipo de ocorrência com o nome informado."""
