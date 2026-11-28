"""Testes da restrição de contas por administradores (HU14)."""

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
    """HU14 C2: somente administrador restringe contas."""
    usuario = logar_como("usuario")

    response = usuario.put("/contas/1/restricao", json={"restrita": True})

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_restringir_conta_inexistente_retorna_404(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C3: não é possível restringir uma conta que não existe."""
    administrador = logar_como("administrador")

    response = administrador.put("/contas/9999/restricao", json={"restrita": True})

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Conta inexistente."}


def test_restringir_conta_sem_campo_restrita_retorna_400(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """O corpo precisa dizer se a restrição deve ser aplicada ou removida."""
    administrador = logar_como("administrador")

    response = administrador.put("/contas/1/restricao", json={})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Dados inválidos."}


def test_administrador_aplica_restricao_em_conta(
    conta_alvo: int,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C7: o administrador marca a conta como restrita."""
    administrador = logar_como("administrador")

    response = administrador.put(
        f"/contas/{conta_alvo}/restricao", json={"restrita": True}
    )

    assert response.status_code == 200
    assert response.get_json() == {"id": conta_alvo, "restrita": True}


def test_aplicar_restricao_em_conta_ja_restrita_nao_altera_nada(
    conta_alvo: int,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C6: repetir a restrição mantém a conta restrita, sem erro."""
    administrador = logar_como("administrador")
    administrador.put(f"/contas/{conta_alvo}/restricao", json={"restrita": True})

    response = administrador.put(
        f"/contas/{conta_alvo}/restricao", json={"restrita": True}
    )

    assert response.status_code == 200
    assert response.get_json() == {"id": conta_alvo, "restrita": True}


def test_administrador_remove_restricao_de_conta_restrita(
    conta_alvo: int,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C5: o administrador libera uma conta que estava restrita."""
    administrador = logar_como("administrador")
    administrador.put(f"/contas/{conta_alvo}/restricao", json={"restrita": True})

    response = administrador.put(
        f"/contas/{conta_alvo}/restricao",
        json={"restrita": False},
    )

    assert response.status_code == 200
    assert response.get_json() == {"id": conta_alvo, "restrita": False}


def test_remover_restricao_de_conta_sem_restricao_retorna_409(
    conta_alvo: int,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU14 C4: não há o que remover em uma conta que não está restrita."""
    administrador = logar_como("administrador")

    response = administrador.put(
        f"/contas/{conta_alvo}/restricao",
        json={"restrita": False},
    )

    assert response.status_code == 409
    assert response.get_json() == {"erro": "Conta não possui restrição."}
