"""Endpoints de gerenciamento das regiões permitidas."""

from flask import Blueprint, Response

from app.auth import nao_autenticado

regiao_bp = Blueprint("regiao", __name__)


@regiao_bp.post("/regioes")
def cadastrar_regiao() -> tuple[Response, int]:
    """Cadastra uma região em que o registro de ocorrências é permitido."""

    return nao_autenticado()
