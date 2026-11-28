"""Autenticação e autorização compartilhadas pelas rotas da API."""

from flask import Response, jsonify, session

from app.conta.conta_model import Conta
from app.conta.conta_service import obter_conta
from app.db import get_db


def conta_autenticada() -> Conta | None:
    """Devolve a conta da sessão atual, ou None se não houver conta válida."""

    conta_id = session.get("conta_id")
    if conta_id is None:
        return None

    return obter_conta(get_db(), conta_id)


def nao_autenticado() -> tuple[Response, int]:
    """Resposta padrão para operações que exigem login."""

    return jsonify({"erro": "Não autenticado."}), 401


def acesso_negado() -> tuple[Response, int]:
    """Resposta padrão para quem está logado, mas não tem o papel exigido."""

    return jsonify({"erro": "Sem permissão."}), 403


def verificar_acesso(papel: str) -> tuple[Response, int] | None:
    """Devolve a resposta 401/403 se o acesso for negado, ou None se permitido."""

    conta = conta_autenticada()
    if conta is None:
        return nao_autenticado()

    if conta.papel != papel:
        return acesso_negado()

    return None
