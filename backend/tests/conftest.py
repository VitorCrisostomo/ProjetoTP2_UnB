"""Fixtures compartilhadas pelos testes."""

from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.db import init_db


@pytest.fixture
def app(tmp_path: Path) -> Flask:
    """Cria uma aplicação com banco SQLite temporário e vazio."""
    aplicacao = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "SECRET_KEY": "chave-exclusiva-de-teste",
        }
    )
    with aplicacao.app_context():
        init_db()
    return aplicacao


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Cliente HTTP de teste ligado ao banco temporário."""
    return app.test_client()
