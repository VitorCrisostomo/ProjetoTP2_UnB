"""Modelo de dados da entidade Conta."""

from dataclasses import dataclass

USUARIO = "usuario"
ADMINISTRADOR = "administrador"
PAPEIS = (USUARIO, ADMINISTRADOR)


@dataclass(frozen=True)
class Conta:
    """Representa uma conta cadastrada no sistema."""

    id: int
    nome: str
    email: str
    senha_hash: str
    papel: str = USUARIO
    restrita: bool = False


class ContaNaoEncontradaError(Exception):
    """Indica que a conta procurada não existe."""


class SemRestricaoError(Exception):
    """Indica que a conta não possui restrição a ser removida."""


class EmailJaCadastradoError(Exception):
    """Indica que o e-mail informado já está cadastrado."""


class DadosInvalidosError(Exception):
    """Indica que os dados fornecidos são inválidos."""
