"""Endpoints de gerenciamento das regiões permitidas."""

from flask import Blueprint, Response, jsonify

from app.auth import verificar_acesso
from app.conta.conta_model import ADMINISTRADOR

regiao_bp = Blueprint("regiao", __name__)


@regiao_bp.post("/regioes")
def cadastrar_regiao() -> tuple[Response, int]:
    """Cadastra uma região em que o registro de ocorrências é permitido."""

    negado = verificar_acesso(ADMINISTRADOR)
    if negado is not None:
        return negado

    return jsonify({}), 201
