"""Endpoints relacionados ao gerenciamento de contas."""

from flask import Blueprint, Response, jsonify, request

from app.conta.conta_model import EmailJaCadastradoError
from app.conta.conta_service import cadastrar_conta
from app.db import get_db

conta_bp = Blueprint("conta", __name__)


@conta_bp.post("/contas")
def criar_conta() -> tuple[Response, int]:
    """Recebe uma solicitação de cadastro de conta."""
    dados = request.get_json()

    try:
        conta = cadastrar_conta(
            get_db(),
            dados["nome"],
            dados["email"],
            dados["senha"],
        )
    except EmailJaCadastradoError:
        return jsonify({"erro": "E-mail já cadastrado."}), 409

    return jsonify(
        {
            "id": conta.id,
            "nome": conta.nome,
            "email": conta.email,
        }
    ), 201
