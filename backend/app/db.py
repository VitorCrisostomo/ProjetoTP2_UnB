"""Conexões SQLite por contexto e inicialização não destrutiva do banco."""

import sqlite3
from typing import cast

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext

from app.conta.conta_repository import criar_tabela_contas
from app.tipo.tipo_repository import criar_tabela_tipos


def get_db() -> sqlite3.Connection:
    """Obtém a conexão do contexto atual, habilitando chaves estrangeiras."""
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return cast(sqlite3.Connection, g.db)


def close_db(exception: BaseException | None = None) -> None:
    """Fecha a conexão ao encerrar o contexto da aplicação."""
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    """Inicializa o banco de dados sem apagar registros existentes."""
    conexao = get_db()
    criar_tabela_contas(conexao)
    criar_tabela_tipos(conexao)
    conexao.commit()


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Inicializa o arquivo SQLite configurado para a aplicação."""
    init_db()
    click.echo("Banco SQLite inicializado.")


def init_app(app: Flask) -> None:
    """Registra o fechamento da conexão e o comando init-db."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
