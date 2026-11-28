"""Endpoints de gerenciamento dos tipos de ocorrência."""

from flask import Blueprint, Response, jsonify, request

from app.auth import acesso_negado, conta_autenticada, nao_autenticado
from app.conta.conta_model import MODERADOR, DadosInvalidosError
from app.db import get_db
from app.tipo.tipo_model import TipoJaExisteError, TipoOcorrencia
from app.tipo.tipo_service import criar_tipo, listar_tipos

tipo_bp = Blueprint("tipo", __name__)


def _dados_tipo(tipo: TipoOcorrencia) -> dict[str, object]:
    """Dados de um tipo de ocorrência como devolvidos pela API."""

    return {"id": tipo.id, "nome": tipo.nome, "ativo": tipo.ativo}


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
        tipo = criar_tipo(get_db(), nome)
    except DadosInvalidosError as erro:
        return jsonify({"erro": str(erro)}), 400
    except TipoJaExisteError as erro:
        return jsonify({"erro": str(erro)}), 409

    return jsonify(_dados_tipo(tipo)), 201


@tipo_bp.get("/tipos")
def listar_tipos_disponiveis() -> tuple[Response, int]:
    """Lista os tipos de ocorrência ativos."""

    tipos = listar_tipos(get_db())

    return jsonify([_dados_tipo(tipo) for tipo in tipos]), 200
