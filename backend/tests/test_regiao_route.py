"""Testes dos endpoints de regiões permitidas (HU18)."""

from flask.testing import FlaskClient


def test_cadastrar_regiao_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU18 C1: usuário não autenticado não define regiões."""
    response = client.post("/regioes", json={"nome": "Plano Piloto"})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_cadastrar_regiao_como_usuario_comum_retorna_403(usuario: FlaskClient) -> None:
    """HU18 C2: somente administrador define regiões."""
    response = usuario.post("/regioes", json={"nome": "Plano Piloto"})

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_cadastrar_regiao_sem_limites_retorna_400(
    administrador: FlaskClient,
) -> None:
    """HU18 C3: a região precisa informar os quatro limites."""
    response = administrador.post("/regioes", json={"nome": "Plano Piloto"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Região inválida."}
