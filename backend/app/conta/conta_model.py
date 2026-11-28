"""Modelo de dados da entidade Conta."""

from dataclasses import dataclass

USUARIO = "usuario"
MODERADOR = "moderador"
ADMINISTRADOR = "administrador"
PAPEIS = (USUARIO, MODERADOR, ADMINISTRADOR)


@dataclass(frozen=True)
class Conta:
    """Representa uma conta cadastrada no sistema."""

    id: int
    nome: str
    email: str
    senha_hash: str
    papel: str = USUARIO


class ContaNaoEncontradaError(Exception):
    """Indica que a conta procurada não existe."""


class EmailJaCadastradoError(Exception):
    """Indica que o e-mail informado já está cadastrado."""


class DadosInvalidosError(Exception):
    """Indica que os dados fornecidos são inválidos."""
