"""Testes dos endpoints de tipos de ocorrência (HU15)."""

from collections.abc import Callable

from flask.testing import FlaskClient


def test_cadastrar_tipo_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU15 C1: usuário não autenticado não cadastra tipos."""
    response = client.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_cadastrar_tipo_como_usuario_comum_retorna_403(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C2: somente moderador cadastra tipos."""
    usuario = logar_como("usuario")

    response = usuario.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_cadastrar_tipo_com_nome_vazio_retorna_400(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C3: o nome do tipo é obrigatório."""
    moderador = logar_como("moderador")

    response = moderador.post("/tipos", json={"nome": "  "})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Nome inválido."}
