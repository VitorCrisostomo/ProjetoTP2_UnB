"""Verifique os exemplos executando as funções do código-fonte."""

import pytest

from exemplo_tipos import saudacao, somar


@pytest.mark.parametrize(
    ("a", "b", "esperado"),
    [(2, 2, 4), (10, -3, 7), (-2, -3, -5), (0, 0, 0)],
)
def test_somar(a: int, b: int, esperado: int) -> None:
    assert somar(a, b) == esperado


@pytest.mark.parametrize(
    ("nome", "esperado"), [("Ana", "Olá, Ana!"), ("João", "Olá, João!")]
)
def test_saudacao(nome: str, esperado: str) -> None:
    assert saudacao(nome) == esperado
