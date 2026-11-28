"""Endpoints de gerenciamento dos tipos de ocorrência."""

from flask import Blueprint, Response

from app.auth import nao_autenticado

tipo_bp = Blueprint("tipo", __name__)


@tipo_bp.post("/tipos")
def cadastrar_tipo() -> tuple[Response, int]:
    """Cadastra um novo tipo de ocorrência (somente moderadores)."""

    return nao_autenticado()
