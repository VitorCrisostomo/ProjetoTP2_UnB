"""Modelo de dados da entidade Conta."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Conta:
    """Representa uma conta cadastrada no sistema."""

    id: int
    nome: str
    email: str
    senha_hash: str
    papel: str = "usuario"


class EmailJaCadastradoError(Exception):
    """Indica que o e-mail informado já está cadastrado."""


class DadosInvalidosError(Exception):
    """Indica que os dados fornecidos são inválidos."""
