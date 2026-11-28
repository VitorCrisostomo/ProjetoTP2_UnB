"""Endpoints de gerenciamento das regiões permitidas."""

from flask import Blueprint, Response, jsonify, request

from app.auth import verificar_acesso
from app.conta.conta_model import ADMINISTRADOR, DadosInvalidosError
from app.regiao.regiao_service import validar_regiao

regiao_bp = Blueprint("regiao", __name__)


@regiao_bp.post("/regioes")
def cadastrar_regiao() -> tuple[Response, int]:
    """Cadastra uma região em que o registro de ocorrências é permitido."""

    negado = verificar_acesso(ADMINISTRADOR)
    if negado is not None:
        return negado

    try:
        validar_regiao(request.get_json(silent=True))
    except DadosInvalidosError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify({}), 201
