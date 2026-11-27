"""Testes de exclusão e edição da própria conta."""

from flask.testing import FlaskClient


def test_excluir_conta_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU03 C1: usuário não autenticado não pode excluir conta."""
    response = client.delete("/conta")

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}

def test_excluir_conta_sem_confirmacao_mantem_a_conta(
    client: FlaskClient,
    conta_logada: dict[str, str],
) -> None:
    """HU03 C2: sem confirmação, a conta não é excluída."""
    response = client.delete("/conta")

    assert response.status_code == 200
    assert response.get_json() == {"excluida": False}
    login = client.post(
        "/login",
        json={"email": conta_logada["email"], "senha": conta_logada["senha"]},
    )
    assert login.status_code == 200
