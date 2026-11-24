Desenvolvimento local
========================

Preparação
----------

Use Python 3.14 e Git. A versão validada do interpretador é 3.14.7. Execute os
comandos abaixo a partir da pasta ``backend``, com o ambiente virtual ativado.
O arquivo ``backend/README.md`` contém o procedimento completo para Windows,
Linux e macOS, incluindo a criação e ativação do ambiente.

.. code-block:: console

   python --version
   python -m pip install -r requirements.txt
   python -m pip check

O SQLite está disponível no módulo ``sqlite3`` do Python; não é necessário
instalar um servidor de banco de dados para preparar o ambiente.

Verificações
------------

.. code-block:: console

   python -m ruff check .
   python -m ruff format --check .
   python -m mypy .
   python -m pytest
   python -m sphinx -b html -n -W --keep-going docs/source docs/build/html

Os testes medem linhas e ramificações do código Python do backend, com limite
mínimo de 80%. Testes, documentação e ambiente virtual não entram na medição.
A cobertura dos exemplos não demonstra atendimento às historietas do projeto.

Para gerar também um relatório HTML de cobertura:

.. code-block:: console

   python -m pytest --cov-report=html --cov-report=term-missing

O relatório fica em ``htmlcov/index.html``. A documentação fica em
``docs/build/html/index.html``. Os resultados gerados não são versionados.

Fluxo de trabalho
--------------------

Escreva um teste que exercite o comportamento esperado, confirme sua falha,
implemente o necessário e refatore mantendo os testes aprovados. Atualize as
docstrings e a referência da API quando criar novos módulos.

Use anotações de tipo, docstrings no estilo Google e a configuração de Ruff do
projeto, com linhas de até 88 caracteres. Para aplicar a formatação localmente,
execute ``python -m ruff format .`` e revise o diff antes de versionar.

As bibliotecas e ferramentas têm versões fixadas em ``requirements.txt``.
Mudanças nesse arquivo devem ser verificadas em um ambiente virtual novo antes
de serem compartilhadas com o grupo.
