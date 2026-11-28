"""Endpoints de gerenciamento dos tipos de ocorrência."""

from flask import Blueprint, Response, jsonify, request

from app.auth import acesso_negado, conta_autenticada, nao_autenticado
from app.conta.conta_model import MODERADOR, DadosInvalidosError
from app.tipo.tipo_service import validar_nome_tipo

tipo_bp = Blueprint("tipo", __name__)


@tipo_bp.post("/tipos")
def cadastrar_tipo() -> tuple[Response, int]:
    """Cadastra um novo tipo de ocorrência (somente moderadores)."""

    conta = conta_autenticada()
    if conta is None:
        return nao_autenticado()

    if conta.papel != MODERADOR:
        return acesso_negado()

    dados = request.get_json(silent=True)
    nome = dados.get("nome") if isinstance(dados, dict) else None

    try:
        validar_nome_tipo(nome)
    except DadosInvalidosError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify({}), 201
