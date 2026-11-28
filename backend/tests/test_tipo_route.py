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


def test_cadastrar_tipo_valido_retorna_201_com_tipo_ativo(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C5: o tipo é criado ativo e devolvido com seu identificador."""
    moderador = logar_como("moderador")

    response = moderador.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 201
    dados = response.get_json()
    assert dados["nome"] == "Buraco"
    assert dados["ativo"] is True
    assert isinstance(dados["id"], int)


def test_cadastrar_tipo_duplicado_retorna_409(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C4: não podem existir dois tipos com o mesmo nome."""
    moderador = logar_como("moderador")
    moderador.post("/tipos", json={"nome": "Buraco"})

    response = moderador.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 409
    assert response.get_json() == {"erro": "Tipo já existe."}


def test_listar_tipos_devolve_os_tipos_ativos_sem_exigir_login(
    client: FlaskClient,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15: qualquer pessoa consulta a lista de tipos disponíveis."""
    moderador = logar_como("moderador")
    moderador.post("/tipos", json={"nome": "Buraco"})
    moderador.post("/tipos", json={"nome": "Alagamento"})

    response = client.get("/tipos")

    assert response.status_code == 200
    nomes = [tipo["nome"] for tipo in response.get_json()]
    assert nomes == ["Buraco", "Alagamento"]


def test_renomear_tipo_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU15 (alterar nome) C1: usuário não autenticado não altera tipos."""
    response = client.put("/tipos/1", json={"nome": "Novo"})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}
