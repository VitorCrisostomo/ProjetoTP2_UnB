Backend executável
==================

Preparação no Windows 11
------------------------

Com Python instalado, abra o PowerShell na raiz do repositório:

.. code-block:: powershell

   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m pip check

Se a ativação estiver bloqueada, use diretamente
``.\.venv\Scripts\python.exe`` no lugar de ``python`` nos comandos abaixo.
A verificação desta alteração foi realizada com Python 3.14.7;
o alvo 3.11 de Ruff e mypy é uma configuração de análise, não uma
garantia de compatibilidade das dependências com Python 3.11.

Execução
--------

Execute os comandos abaixo dentro de ``backend``, após instalar
``requirements.txt`` no ambiente virtual:

.. code-block:: powershell

   python -m flask --app app init-db
   python -m flask --app app run --debug

O servidor de desenvolvimento responde em http://127.0.0.1:5000/health
com ``{"status": "ok"}``. Essa rota verifica somente o servidor HTTP.
O servidor de desenvolvimento não deve ser usado em produção.

O comando ``init-db`` cria ``backend/instance/tp2.sqlite3`` sem apagar dados.
O esquema de domínio será definido quando os requisitos estiverem disponíveis;
esta estrutura não implementa cadastro ou gerenciamento de ocorrências.
Conexões SQLite são fechadas ao encerrar cada contexto da aplicação.

Verificações
------------

.. code-block:: powershell

   python -m pytest
   python -m ruff check .
   python -m ruff format --check .
   python -m mypy .
   python -m sphinx -W --keep-going -b html docs/source docs/build/html

A cobertura mede o pacote ``app``, incluindo ramificações, com mínimo de 80%.
Os testes utilizam banco temporário e verificam persistência, fechamento
da conexão e reinicialização sem perda de dados.

API interna
-----------

.. automodule:: app
   :members:

.. automodule:: app.db
   :members:
