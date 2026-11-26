"""Fábrica da aplicação Flask do Projeto TP2."""

from pathlib import Path
from typing import Any

from flask import Flask

from app import db
from app.conta.conta_route import conta_bp


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Cria uma aplicação com configuração e banco isoláveis para testes."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(DATABASE=str(Path(app.instance_path) / "tp2.sqlite3"))
    if test_config is not None:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    app.register_blueprint(conta_bp)

    @app.get("/health")
    def health() -> dict[str, str]:
        """Informa que o servidor está respondendo."""
        return {"status": "ok"}

    return app
