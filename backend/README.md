# Desenvolvimento do backend

Este diretório reúne o ambiente Python do sistema de ocorrências do projeto de
Técnicas de Programação 2 da UnB. O objetivo deste guia é permitir que os quatro
integrantes instalem as mesmas dependências e executem testes, análise de código
e documentação antes de implementar as funcionalidades.

## Pré-requisitos

- [Git](https://git-scm.com/downloads) instalado.
- [Python 3.14](https://www.python.org/downloads/) instalado. O ambiente foi
  validado com **Python 3.14.7**; use a série **3.14.x** no desenvolvimento.
- Acesso à internet para clonar o repositório e instalar as dependências.

O Sphinx fixado em `requirements.txt` exige Python 3.13 ou superior. Python 3.11
não instala o conjunto atual de dependências. A versão adotada pela equipe é
Python 3.14, também utilizada nas configurações do Ruff e do mypy.

SQLite já acompanha o Python por meio do módulo `sqlite3`; não é necessário
instalar um servidor de banco de dados para preparar o ambiente.

## Obter o projeto

Se você ainda não tem uma cópia local:

```text
git clone https://github.com/VitorCrisostomo/ProjetoTP2_UnB.git
cd ProjetoTP2_UnB/backend
```

Se já tem uma cópia, entre na pasta `backend` desse checkout. Execute os próximos
comandos nessa pasta, onde estão `requirements.txt` e `pyproject.toml`.

## Instalar no Windows com PowerShell

Confira o interpretador e crie um ambiente virtual exclusivo para o backend:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install -r requirements.txt
python -m pip check
```

Se o PowerShell bloquear a ativação, use diretamente o Python do ambiente virtual.
Isso dispensa alterações na política de execução:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest
```

Nos demais comandos deste guia, substitua `python` por
`.\.venv\Scripts\python.exe` quando o ambiente não estiver ativado.

## Instalar no Linux ou macOS

Com Python 3.14 disponível no sistema:

```bash
python3.14 --version
python3.14 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m pip check
```

Se sua distribuição fornecer o módulo `venv` separadamente, instale o suporte a
ambientes virtuais correspondente ao Python 3.14 antes de criar `.venv`.

Em qualquer sistema, confira o interpretador selecionado:

```text
python -c "import sys; print(sys.executable); print(sys.version)"
```

O executável deve estar dentro de `backend/.venv`. No editor, selecione esse mesmo
interpretador para análise de tipos, testes e execução de arquivos.

## Ferramentas disponíveis

As versões exatas, incluindo dependências transitivas, estão em
[`requirements.txt`](requirements.txt). A configuração compartilhada das
verificações está em [`pyproject.toml`](pyproject.toml).

| Ferramenta | Finalidade |
| --- | --- |
| Flask | Framework escolhido para a API do backend. |
| SQLite / `sqlite3` | Persistência local prevista para a aplicação. |
| pytest | Execução dos testes automatizados. |
| pytest-cov / coverage | Medição de cobertura, incluindo ramificações. |
| Ruff | Análise de código, organização de imports e formatação. |
| mypy | Verificação estática de tipos em modo estrito. |
| Sphinx | Geração da documentação técnica a partir de reStructuredText e docstrings. |

## Verificações antes de compartilhar mudanças

Com o ambiente virtual ativado e o terminal em `backend`, execute:

```text
python -m pip check
python -m ruff check .
python -m ruff format --check .
python -m mypy .
python -m pytest
python -m sphinx -b html -n -W --keep-going docs/source docs/build/html
```

Todos os comandos devem terminar com código de saída zero. O Ruff em modo
`--check` apenas informa diferenças de formatação. Para aplicar a formatação aos
arquivos locais:

```text
python -m ruff format .
```

Depois, revise as diferenças e repita as verificações afetadas pela mudança.
Os comandos de análise e teste não fazem commit nem enviam arquivos ao GitHub.

## Testes e cobertura

O `pytest` descobre os testes em `tests/`. A configuração já ativa cobertura,
relatório no terminal e exigência mínima de **80%**; portanto, o comando padrão é:

```text
python -m pytest
```

Para executar um teste específico durante o desenvolvimento:

```text
python -m pytest tests/test_exemplo.py
```

O limite de cobertura também se aplica às execuções parciais. Para um ciclo rápido
de um único teste, sem medir cobertura nessa execução:

```text
python -m pytest tests/test_exemplo.py --no-cov
```

Antes de compartilhar o trabalho, execute novamente a suíte completa com a
cobertura padrão. Para gerar um relatório navegável:

```text
python -m pytest --cov-report=html
```

Abra `htmlcov/index.html` no navegador. Relatórios, caches e ambientes virtuais são
arquivos locais de desenvolvimento e devem permanecer fora do versionamento.

A cobertura inclui o código Python dentro de `backend`, excluindo testes,
documentação e o ambiente virtual. Essa origem também deve incluir os módulos
de produção que forem adicionados ao diretório. Hoje, o código medido é o módulo
`exemplo_tipos`; a cobertura dos exemplos não comprova funcionalidades ainda não
implementadas. Ao alterar a estrutura do projeto, revise as inclusões e exclusões
em `pyproject.toml` para manter todo o código de produção na medição.

O fluxo recomendado para cada historieta é:

1. Definir o comportamento esperado e seus casos de erro.
2. Escrever um teste que importe e exercite o código responsável por esse comportamento.
3. Executar o teste e confirmar que falha pelo motivo esperado.
4. Implementar o comportamento até o teste passar.
5. Refatorar e executar a suíte completa, a análise estática e a formatação.

Testes devem verificar regras da aplicação. Asserções aritméticas isoladas não
testam as funções do projeto. Adicione anotações de tipo ao código e aos testes,
conforme a configuração estrita do mypy.

## Documentação técnica

Os arquivos-fonte ficam em `docs/source/`. Para gerar o HTML com avisos tratados
como erros:

```text
python -m sphinx -b html -n -W --keep-going docs/source docs/build/html
```

Abra `docs/build/html/index.html` no navegador. Não é necessário instalar `make`
para usar esse comando.

Ao acrescentar módulos públicos, escreva docstrings e inclua as respectivas
referências na documentação Sphinx. As extensões `autodoc`, `napoleon`
e `viewcode` estão disponíveis. Use docstrings no estilo Google. Mantenha as
instruções de instalação e os comandos deste README atualizados quando a estrutura
do backend mudar.

## Estado atual e início da implementação

O backend contém ferramentas de desenvolvimento e um módulo de exemplo com
testes. Flask está instalado, mas a aplicação, os endpoints e o esquema de banco
do sistema de ocorrências ainda precisam ser implementados neste checkout.
Não há, nesta preparação, um comando de inicialização da API ou de criação das
tabelas de negócio.

Antes de iniciar uma funcionalidade, combine com a equipe o contrato da API, as
permissões, os dados persistidos e os critérios de aceitação da historieta.
Implemente os testes junto com o código e documente o comando de execução quando
a aplicação Flask for adicionada.

## Alterar dependências com segurança

Para reproduzir o ambiente, use sempre o arquivo versionado:

```text
python -m pip install -r requirements.txt
python -m pip check
```

Uma nova dependência deve ter finalidade definida, licença compatível com as
regras do trabalho e validação da equipe. Atualize as versões fixadas em um
ambiente virtual dedicado ao projeto e execute todas as verificações depois.
Não substitua `requirements.txt` por um `pip freeze` de um Python global ou de um
ambiente que contenha ferramentas de outros projetos.

## Problemas comuns

| Sintoma | O que conferir |
| --- | --- |
| `py -3.14` ou `python3.14` não encontrado | Instale Python 3.14 e reabra o terminal. |
| Instalação do Sphinx falha por versão do Python | Confira `python --version`; o conjunto foi padronizado em 3.14. |
| Ambiente virtual foi criado com outro Python | Desative-o, preserve os arquivos de trabalho e recrie `.venv` usando Python 3.14. |
| Módulo ou comando de ferramenta não encontrado | Confira `sys.executable` e instale `requirements.txt` nesse interpretador. |
| Testes não encontram o módulo local | Execute a partir de `backend`, usando o `pyproject.toml` desse diretório. |
| Cobertura abaixo de 80% | Leia o relatório e acrescente testes para os comportamentos e caminhos ainda não exercitados. |
| Sphinx retorna erro | Corrija os avisos exibidos; `-W` transforma avisos em falha para manter a documentação verificável. |

Para sair do ambiente virtual ativado:

```text
deactivate
```
