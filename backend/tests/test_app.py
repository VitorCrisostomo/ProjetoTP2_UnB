"""Testes de execução, configuração e ciclo de vida do SQLite."""

import sqlite3
from pathlib import Path

import pytest

from app import create_app
from app.db import get_db


def test_health() -> None:
    app = create_app({"TESTING": True, "DATABASE": ":memory:"})
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    assert app.test_client().get("/inexistente").status_code == 404


def test_default_database() -> None:
    app = create_app()
    assert app.config["DATABASE"] == str(Path(app.instance_path) / "tp2.sqlite3")


def test_database_lifecycle(tmp_path: Path) -> None:
    database = tmp_path / "test.sqlite3"
    app = create_app({"TESTING": True, "DATABASE": str(database)})
    runner = app.test_cli_runner()
    result = runner.invoke(args=["init-db"])
    assert result.exit_code == 0
    assert "inicializado" in result.output
    assert database.is_file()
    with app.app_context():
        connection = get_db()
        assert get_db() is connection
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        connection.execute("CREATE TABLE exemplo (valor TEXT NOT NULL)")
        connection.execute("INSERT INTO exemplo VALUES (?)", ("persistido",))
        connection.commit()
    with pytest.raises(sqlite3.ProgrammingError):
        connection.execute("SELECT 1")
    assert runner.invoke(args=["init-db"]).exit_code == 0
    with app.app_context():
        assert (
            get_db().execute("SELECT valor FROM exemplo").fetchone()[0] == "persistido"
        )
