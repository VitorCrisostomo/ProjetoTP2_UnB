"""Comandos de linha de comando para administrar contas."""

import click
from flask.cli import with_appcontext

from app.conta.conta_model import ContaNaoEncontradaError, DadosInvalidosError
from app.conta.conta_service import definir_papel
from app.db import get_db


@click.command("definir-papel")
@click.argument("email")
@click.argument("papel")
@with_appcontext
def definir_papel_command(email: str, papel: str) -> None:
    """Define o papel (usuario ou administrador) de uma conta."""
    try:
        definir_papel(get_db(), email, papel)
    except (DadosInvalidosError, ContaNaoEncontradaError) as erro:
        raise click.ClickException(str(erro)) from erro

    click.echo("Papel atualizado.")
