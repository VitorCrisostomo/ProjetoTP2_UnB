"""Regras de negócio das regiões permitidas."""

from app.conta.conta_model import DadosInvalidosError


def _numero(valor: object) -> float:
    """Converte um valor numérico (não booleano) em float."""

    if isinstance(valor, bool) or not isinstance(valor, int | float):
        raise DadosInvalidosError("Região inválida.")

    return float(valor)


def validar_regiao(dados: object) -> tuple[str, float, float, float, float]:
    """Valida os dados de uma região e devolve o nome e os quatro limites."""

    if not isinstance(dados, dict):
        raise DadosInvalidosError("Região inválida.")

    nome = dados.get("nome")
    if not isinstance(nome, str) or not nome.strip():
        raise DadosInvalidosError("Região inválida.")

    lat_min = _numero(dados.get("lat_min"))
    lat_max = _numero(dados.get("lat_max"))
    lon_min = _numero(dados.get("lon_min"))
    lon_max = _numero(dados.get("lon_max"))

    return nome.strip(), lat_min, lat_max, lon_min, lon_max
