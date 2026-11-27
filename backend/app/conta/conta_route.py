"""Endpoints relacionados ao gerenciamento de contas."""

from flask import Blueprint, Response, jsonify, request, session

from app.conta.conta_model import (
    DadosInvalidosError,
    EmailJaCadastradoError,
)
from app.conta.conta_service import autenticar_conta, cadastrar_conta
from app.db import get_db

conta_bp = Blueprint("conta", __name__)


@conta_bp.post("/contas")
def criar_conta() -> tuple[Response, int]:
    """Recebe uma solicitação de cadastro de conta."""

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados inválidos."}), 400

    try:
        conta = cadastrar_conta(
            get_db(),
            dados.get("nome"),
            dados.get("email"),
            dados.get("senha"),
        )

    except DadosInvalidosError as erro:
        return jsonify({"erro": str(erro)}), 400

    except EmailJaCadastradoError:
        return jsonify({"erro": "E-mail já cadastrado."}), 409

    return jsonify(
        {
            "id": conta.id,
            "nome": conta.nome,
            "email": conta.email,
        }
    ), 201


@conta_bp.post("/login")
def login() -> tuple[Response, int]:
    """Autentica o usuário e estabelece uma sessão."""

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados inválidos."}), 400

    try:
        conta = autenticar_conta(
            get_db(),
            dados.get("email"),
            dados.get("senha"),
        )

    except DadosInvalidosError as erro:
        return jsonify({"erro": str(erro)}), 400

    if conta is None:
        return jsonify({"erro": "Credenciais inválidas."}), 401

    session.clear()
    session["conta_id"] = conta.id

    return jsonify(
        {
            "id": conta.id,
            "nome": conta.nome,
            "email": conta.email,
        }
    ), 200


@conta_bp.delete("/conta")
def excluir_conta_logada() -> tuple[Response, int]:
    """Exclui a conta do usuário autenticado após confirmação."""

    if "conta_id" not in session:
        return jsonify({"erro": "Não autenticado."}), 401

    return jsonify({"excluida": False}), 200
