"""Testes dos endpoints de regiões permitidas (HU18)."""

from flask.testing import FlaskClient


def test_cadastrar_regiao_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU18 C1: usuário não autenticado não define regiões."""
    response = client.post("/regioes", json={"nome": "Plano Piloto"})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}
