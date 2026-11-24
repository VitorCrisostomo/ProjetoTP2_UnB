"""Exemplos pequenos para validar tipagem, testes e documentação do ambiente."""


def somar(a: int, b: int) -> int:
    """Some dois números inteiros.

    Args:
        a: Primeiro número.
        b: Segundo número.

    Returns:
        A soma dos argumentos.
    """
    return a + b


def saudacao(nome: str) -> str:
    """Crie uma saudação para o nome informado.

    Args:
        nome: Nome usado na mensagem.

    Returns:
        Mensagem de saudação.
    """
    return f"Olá, {nome}!"
