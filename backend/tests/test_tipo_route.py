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
    """HU15 C2: somente administrador cadastra tipos."""
    usuario = logar_como("usuario")

    response = usuario.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_cadastrar_tipo_com_nome_vazio_retorna_400(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C3: o nome do tipo é obrigatório."""
    administrador = logar_como("administrador")

    response = administrador.post("/tipos", json={"nome": "  "})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Nome inválido."}


def test_cadastrar_tipo_valido_retorna_201_com_tipo_ativo(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C5: o tipo é criado ativo e devolvido com seu identificador."""
    administrador = logar_como("administrador")

    response = administrador.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 201
    dados = response.get_json()
    assert dados["nome"] == "Buraco"
    assert dados["ativo"] is True
    assert isinstance(dados["id"], int)


def test_cadastrar_tipo_duplicado_retorna_409(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 C4: não podem existir dois tipos com o mesmo nome."""
    administrador = logar_como("administrador")
    administrador.post("/tipos", json={"nome": "Buraco"})

    response = administrador.post("/tipos", json={"nome": "Buraco"})

    assert response.status_code == 409
    assert response.get_json() == {"erro": "Tipo já existe."}


def test_listar_tipos_devolve_os_tipos_ativos_sem_exigir_login(
    client: FlaskClient,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15: qualquer pessoa consulta a lista de tipos disponíveis."""
    administrador = logar_como("administrador")
    administrador.post("/tipos", json={"nome": "Buraco"})
    administrador.post("/tipos", json={"nome": "Alagamento"})

    response = client.get("/tipos")

    assert response.status_code == 200
    nomes = [tipo["nome"] for tipo in response.get_json()]
    assert nomes == ["Buraco", "Alagamento"]


def test_renomear_tipo_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU15 (alterar nome) C1: usuário não autenticado não altera tipos."""
    response = client.put("/tipos/1", json={"nome": "Novo"})

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_renomear_tipo_como_usuario_comum_retorna_403(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (alterar nome) C2: somente administrador altera tipos."""
    usuario = logar_como("usuario")

    response = usuario.put("/tipos/1", json={"nome": "Novo"})

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_renomear_tipo_inexistente_retorna_404(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (alterar nome) C3: não é possível renomear um tipo que não existe."""
    administrador = logar_como("administrador")

    response = administrador.put("/tipos/9999", json={"nome": "Novo"})

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Tipo inexistente."}


def test_renomear_tipo_com_nome_vazio_retorna_400(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (alterar nome) C4: o novo nome não pode ser vazio."""
    administrador = logar_como("administrador")
    tipo_id = administrador.post("/tipos", json={"nome": "Buraco"}).get_json()["id"]

    response = administrador.put(f"/tipos/{tipo_id}", json={"nome": ""})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Nome inválido."}


def test_renomear_tipo_para_nome_existente_retorna_409(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (alterar nome) C5: o novo nome não pode repetir outro tipo."""
    administrador = logar_como("administrador")
    administrador.post("/tipos", json={"nome": "Buraco"})
    tipo_id = administrador.post("/tipos", json={"nome": "Alagamento"}).get_json()["id"]

    response = administrador.put(f"/tipos/{tipo_id}", json={"nome": "Buraco"})

    assert response.status_code == 409
    assert response.get_json() == {"erro": "Tipo já existe."}


def test_renomear_tipo_valido_atualiza_o_nome(
    client: FlaskClient,
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (alterar nome) C6: o novo nome é gravado e passa a ser listado."""
    administrador = logar_como("administrador")
    tipo_id = administrador.post("/tipos", json={"nome": "Buraco"}).get_json()["id"]

    response = administrador.put(f"/tipos/{tipo_id}", json={"nome": "Buraco na via"})

    assert response.status_code == 200
    assert response.get_json() == {
        "id": tipo_id,
        "nome": "Buraco na via",
        "ativo": True,
    }
    nomes = [tipo["nome"] for tipo in client.get("/tipos").get_json()]
    assert nomes == ["Buraco na via"]


def test_desativar_tipo_sem_login_retorna_401(client: FlaskClient) -> None:
    """HU15 (desativar) C1: usuário não autenticado não desativa tipos."""
    response = client.post("/tipos/1/desativar")

    assert response.status_code == 401
    assert response.get_json() == {"erro": "Não autenticado."}


def test_desativar_tipo_como_usuario_comum_retorna_403(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (desativar) C2: somente administrador desativa tipos."""
    usuario = logar_como("usuario")

    response = usuario.post("/tipos/1/desativar")

    assert response.status_code == 403
    assert response.get_json() == {"erro": "Sem permissão."}


def test_desativar_tipo_inexistente_retorna_404(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (desativar) C3: não é possível desativar um tipo que não existe."""
    administrador = logar_como("administrador")

    response = administrador.post("/tipos/9999/desativar")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Tipo inexistente."}


def test_desativar_tipo_marca_inativo_e_remove_da_lista(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (desativar) C4: tipo desativado deixa de ser oferecido."""
    administrador = logar_como("administrador")
    tipo_id = administrador.post("/tipos", json={"nome": "Buraco"}).get_json()["id"]

    response = administrador.post(f"/tipos/{tipo_id}/desativar")

    assert response.status_code == 200
    assert response.get_json() == {"id": tipo_id, "nome": "Buraco", "ativo": False}
    assert administrador.get("/tipos").get_json() == []


def test_desativar_tipo_ja_desativado_nao_altera_nada(
    logar_como: Callable[[str], FlaskClient],
) -> None:
    """HU15 (desativar) C5: repetir a desativação não causa erro."""
    administrador = logar_como("administrador")
    tipo_id = administrador.post("/tipos", json={"nome": "Buraco"}).get_json()["id"]
    administrador.post(f"/tipos/{tipo_id}/desativar")

    response = administrador.post(f"/tipos/{tipo_id}/desativar")

    assert response.status_code == 200
    assert response.get_json() == {"id": tipo_id, "nome": "Buraco", "ativo": False}
