"""Testes da restrição de contas por moderadores (HU14)."""

from collections.abc import Callable

from flask.testing import FlaskClient


def test_restringir_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU14 C1: usuário não autenticado não restringe contas."""
    response = client.put("/contas/1/restricao", json={"restrita": True})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_restringir_conta_como_usuario_comum_retorna_403(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C2: somente moderador restringe contas."""
    usuario = logar_como("usuario")

    response = usuario.put("/contas/1/restricao", json={"restrita": True})

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_restringir_conta_inexistente_retorna_404(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C3: não é possível restringir uma conta que não existe."""
    moderador = logar_como("moderador")

    response = moderador.put("/contas/9999/restricao", json={"restrita": True})

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Conta inexistente."}


def test_restringir_conta_sem_campo_restrita_retorna_400(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """O corpo precisa dizer se a restrição deve ser aplicada ou removida."""
    moderador = logar_como("moderador")

    response = moderador.put("/contas/1/restricao", json={})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Dados inválidos."}
