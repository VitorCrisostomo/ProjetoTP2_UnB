"""Endpoints relacionados ao gerenciamento de contas."""

from flask import Blueprint, Response, jsonify, request, session

from app.conta.conta_model import (
    Conta,
    DadosInvalidosError,
    EmailJaCadastradoError,
)
from app.conta.conta_service import (
    atualizar_conta,
    autenticar_conta,
    cadastrar_conta,
    excluir_conta,
    obter_conta,
)
from app.db import get_db

conta_bp = Blueprint("conta", __name__)


def _conta_logada() -> Conta | None:
    """Devolve a conta da sessão atual, ou None se não houver conta válida."""

    conta_id = session.get("conta_id")
    if conta_id is None:
        return None

    return obter_conta(get_db(), conta_id)


def _nao_autenticado() -> tuple[Response, int]:
    """Resposta padrão para operações que exigem login."""

    return jsonify({"erro": "Não autenticado."}), 401


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

    conta = _conta_logada()
    if conta is None:
        return _nao_autenticado()

    dados = request.get_json(silent=True)
    if isinstance(dados, dict) and dados.get("confirmar") is True:
        excluir_conta(get_db(), conta.id)
        session.clear()
        return Response(), 204

    return jsonify({"excluida": False}), 200


@conta_bp.get("/conta")
def consultar_conta() -> tuple[Response, int]:
    """Devolve os dados da conta do usuário autenticado."""

    conta = _conta_logada()
    if conta is None:
        return _nao_autenticado()

    return jsonify({"id": conta.id, "nome": conta.nome, "email": conta.email}), 200


@conta_bp.put("/conta")
def editar_conta_logada() -> tuple[Response, int]:
    """Atualiza os dados da conta do usuário autenticado."""

    conta = _conta_logada()
    if conta is None:
        return _nao_autenticado()

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or dados.get("confirmar") is not True:
        return jsonify({"atualizada": False}), 200

    try:
        atualizar_conta(
            get_db(),
            conta,
            dados.get("nome"),
            dados.get("email"),
            dados.get("senha"),
        )
    except DadosInvalidosError as erro:
        return jsonify({"erro": str(erro)}), 400
    except EmailJaCadastradoError:
        return jsonify({"erro": "E-mail já cadastrado."}), 409

    return jsonify({"atualizada": True}), 200
