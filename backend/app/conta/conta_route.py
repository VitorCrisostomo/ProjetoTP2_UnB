"""Endpoints relacionados ao gerenciamento de contas."""

from flask import Blueprint, Response, jsonify, request, session

from app.auth import conta_autenticada, nao_autenticado, verificar_acesso
from app.conta.conta_model import (
    ADMINISTRADOR,
    Conta,
    ContaNaoEncontradaError,
    DadosInvalidosError,
    EmailJaCadastradoError,
    SemRestricaoError,
)
from app.conta.conta_service import (
    atualizar_conta,
    autenticar_conta,
    cadastrar_conta,
    definir_restricao,
    excluir_conta,
)
from app.db import get_db

conta_bp = Blueprint("conta", __name__)


def _dados_publicos(conta: Conta) -> dict[str, object]:
    """Dados da conta que a API pode devolver (nunca a senha nem o hash)."""

    return {
        "id": conta.id,
        "nome": conta.nome,
        "email": conta.email,
        "papel": conta.papel,
    }


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

    return jsonify(_dados_publicos(conta)), 201


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

    return jsonify(_dados_publicos(conta)), 200


@conta_bp.delete("/conta")
def excluirconta_autenticada() -> tuple[Response, int]:
    """Exclui a conta do usuário autenticado após confirmação."""

    conta = conta_autenticada()
    if conta is None:
        return nao_autenticado()

    dados = request.get_json(silent=True)
    if isinstance(dados, dict) and dados.get("confirmar") is True:
        excluir_conta(get_db(), conta.id)
        session.clear()
        return Response(), 204

    return jsonify({"excluida": False}), 200


@conta_bp.get("/conta")
def consultar_conta() -> tuple[Response, int]:
    """Devolve os dados da conta do usuário autenticado."""

    conta = conta_autenticada()
    if conta is None:
        return nao_autenticado()

    return jsonify(_dados_publicos(conta)), 200


@conta_bp.put("/conta")
def editarconta_autenticada() -> tuple[Response, int]:
    """Atualiza os dados da conta do usuário autenticado."""

    conta = conta_autenticada()
    if conta is None:
        return nao_autenticado()

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or dados.get("confirmar") is not True:
        return jsonify({"atualizada": False}), 200

    try:
        atualizada = atualizar_conta(
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

    return jsonify(_dados_publicos(atualizada)), 200


@conta_bp.put("/contas/<int:conta_id>/restricao")
def definir_restricao_conta(conta_id: int) -> tuple[Response, int]:
    """Aplica ou remove a restrição de acesso de uma conta (administradores)."""

    negado = verificar_acesso(ADMINISTRADOR)
    if negado is not None:
        return negado

    dados = request.get_json(silent=True)
    restrita = dados.get("restrita") if isinstance(dados, dict) else None

    if not isinstance(restrita, bool):
        return jsonify({"erro": "Dados inválidos."}), 400

    try:
        conta = definir_restricao(get_db(), conta_id, restrita)
    except ContaNaoEncontradaError as erro:
        return jsonify({"erro": str(erro)}), 404
    except SemRestricaoError as erro:
        return jsonify({"erro": str(erro)}), 409

    return jsonify({"id": conta.id, "restrita": conta.restrita}), 200
