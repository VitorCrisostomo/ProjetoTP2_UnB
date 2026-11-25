# Desenvolvimento do frontend

Base de desenvolvimento do sistema de ocorrências de Técnicas de Programação 2 da UnB.
A configuração segue a tabela da página 1 de **Especificação Projeto Final TP2**.

## Ferramentas da especificação

| Especificação         | Ferramenta e configuração local                                            |
| --------------------- | -------------------------------------------------------------------------- |
| Linguagem e framework | TypeScript e Next.js com App Router, em `src/app/`.                        |
| Padrão de código      | TypeScript-ESLint e Prettier; `eslint.config.mjs` e `.prettierrc.json`.    |
| Testes                | Vitest; `vitest.config.ts` e `tests/`.                                     |
| Cobertura             | `@vitest/coverage-v8`, provedor V8 do Vitest.                              |
| Análise estática      | ESLint com regras de Next.js e TypeScript-ESLint com informações de tipos. |
| Verificação de tipos  | TypeScript (`tsc --noEmit`), modo estrito.                                 |
| Documentação          | TypeDoc; `typedoc.json`.                                                   |

React e React DOM são dependências do Next.js. React Testing Library, jest-dom,
jsdom e o plugin React do Vite dão suporte a testes de componentes; não são
novas funcionalidades do produto. `eslint-config-prettier` evita conflitos
entre as regras de lint e a formatação.

As regras de Next.js/Core Web Vitals e React Hooks são habilitadas diretamente
por `@next/eslint-plugin-next` e `eslint-plugin-react-hooks`, com versões
compatíveis com o ESLint adotado.

O `npm audit` aponta o aviso moderado
[GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249)
em `minimatch`, dependência de desenvolvimento do TypeDoc. A versão 11.0.1
de `minimatch` elimina o aviso, mas quebra a API usada pelo TypeDoc 0.28.20
(`matchOne`). Portanto, não foi aplicado override incompatível nem downgrade
automático do TypeDoc. Reavalie o aviso quando houver atualização compatível;
execute `npm audit` e `npm run docs` ao atualizar. A documentação deve ser gerada
com arquivos locais confiáveis.

SQLite pertence ao backend: não instale banco, Python ou driver SQLite no frontend.
GitHub/Projects e as IAs declaradas no PDF são serviços de colaboração, não
pacotes npm. Sua utilização não é configurada por esta instalação.

## Pré-requisitos

- [Git](https://git-scm.com/downloads).
- [Node.js](https://nodejs.org/en/download) **26.x** e npm **12.x**.
- Internet para obter o repositório e as dependências.

Versões locais de referência: Node **26.8.1** e npm **12.2.1**. Arquivos
`.nvmrc` e `.node-version` registram o Node adotado; não instalam o interpretador
automaticamente. Se usar um gerenciador de versões, selecione essa versão.
O campo `engines` e `.npmrc` rejeitam versões fora das séries declaradas.

## Obter e instalar

No Windows (PowerShell), Linux ou macOS:

```text
git clone https://github.com/VitorCrisostomo/ProjetoTP2_UnB.git
cd ProjetoTP2_UnB/frontend
node --version
npm --version
npm ci
```

Se o projeto já estiver clonado, apenas entre em `frontend`. Todos os comandos
abaixo devem ser executados nessa pasta.

No PowerShell, se `npm.ps1` for bloqueado, use `npm.cmd` em vez de `npm` em todos
os comandos. Não é necessário mudar a política de execução.

Não crie um ambiente virtual Python: as dependências ficam em `node_modules/`.
Não é necessário instalar Next.js, TypeScript ou Vitest globalmente.

`package.json` fixa as versões diretas; `package-lock.json` fixa a árvore de
dependências. Versione os dois arquivos. Use **npm ci** ao clonar ou sincronizar
o projeto: ele reproduz o lock e substitui a instalação local em `node_modules`.
Se houver divergência entre manifesto e lock, corrija a atualização de
dependências na origem; não apague o lock para contornar o erro.

## Iniciar o desenvolvimento

```text
npm run dev
```

Abra [localhost:3000](http://localhost:3000). As alterações em `src/` são recarregadas.
Encerre com Ctrl+C. Para escolher outra porta:

```text
npm run dev -- --port 3001
```

A página inicial é uma base demonstrativa. Cadastro, login, mapa, estatísticas,
notificações e integração com Flask ainda serão implementados.
A preparação não depende de endpoints do backend nem de serviços externos.
Quando a integração for definida, documente as variáveis em um `.env.example`;
nunca coloque segredos em variáveis `NEXT_PUBLIC_*`, pois chegam ao navegador.

## Comandos de verificação

| Comando                | Resultado esperado                                             |
| ---------------------- | -------------------------------------------------------------- |
| `npm run lint`         | ESLint e TypeScript-ESLint, sem erros nem avisos.              |
| `npm run format:check` | Verifica formatação sem modificar arquivos.                    |
| `npm run typecheck`    | Gera tipos do Next.js e executa `tsc --noEmit`.                |
| `npm test`             | Executa testes uma vez, com cobertura e limite mínimo.         |
| `npm run test:watch`   | Modo interativo para TDD, sem exigir cobertura nessa execução. |
| `npm run docs`         | Gera a referência TypeDoc; avisos fazem o comando falhar.      |
| `npm run build`        | Compila a aplicação de produção.                               |
| `npm run check`        | Executa todas as verificações acima, exceto o modo interativo. |

Para aplicar a formatação, execute `npm run format` e revise o diff.
Convenções: aspas duplas, ponto e vírgula, vírgula final e alvo de 88 caracteres.
Prettier decide as quebras; esse alvo não é um limite absoluto para textos/URLs.

Para reproduzir o fluxo completo de validação:

```text
npm ci
npm run check
```

Para executar a compilação de produção após `npm run build`:

```text
npm start
```

`npm start` exige uma compilação anterior. Encerre o servidor de desenvolvimento
antes de iniciar o de produção na mesma porta.

## Testes, TDD e cobertura

Escreva primeiro um teste que exercite o comportamento esperado e confirme sua
falha. Implemente o necessário, refatore e execute novamente as verificações.
Os testes iniciais renderizam a página real e verificam o idioma/conteúdo do layout.

O provedor V8 mede **todos os arquivos TypeScript/TSX em src**, incluindo os não
importados pelos testes, exceto declarações `.d.ts`. Testes, configurações e
documentação não entram na medição. O mínimo configurado é **80%** para linhas,
funções, ramificações e instruções. Não reduza o escopo para esconder código sem testes.

O relatório HTML fica em `coverage/index.html`. O resumo no terminal e
`coverage/coverage-summary.json` também são gerados.
A cobertura desta base inicial não comprova atendimento às historietas.

Durante o ciclo curto de desenvolvimento:

```text
npm run test:watch
npm run test:watch -- tests/home.test.tsx
```

Antes de compartilhar mudanças, execute `npm run check`.
Vitest cobre componentes síncronos nesta base; funcionalidades com Server
Components assíncronos devem ter estratégia de teste definida ao serem adicionadas.
Testes de navegador e integração com a API não estão incluídos nesta preparação.

## Estrutura e documentação

```text
frontend/
  src/
    app/
      globals.css
      layout.tsx
      page.tsx
    components/
      project-intro.tsx
  tests/
    home.test.tsx
    layout.test.tsx
    setup.ts
  eslint.config.mjs
  next.config.ts
  package.json
  package-lock.json
  tsconfig.json
  typedoc.json
  vitest.config.ts
```

Use `@/` para importar arquivos de `src/`. Escreva código tipado; evite `any` e
documente APIs públicas com comentários TSDoc (`/** ... */`).

`npm run docs` gera `docs/api/index.html`. O TypeDoc documenta os componentes
exportados de `src/components`. Ao criar módulos públicos em outras pastas,
adicione suas entradas em `typedoc.json`. A referência de código não substitui
este guia nem documenta automaticamente todas as telas e decisões da aplicação.

`node_modules/`, `.next/`, `coverage/` e `docs/api/` são gerados e ignorados pelo Git.
O arquivo `next-env.d.ts` é gerenciado pelo Next.js; não o edite manualmente.

## Atualizar dependências

Use `npm ci` para reproduzir e `npm install` somente quando for alterar dependências.
A configuração `save-exact=true` evita intervalos nas novas versões diretas.

```text
npm install --save-exact nome-do-pacote@versao
npm install --save-dev --save-exact nome-da-ferramenta@versao
npm run check
```

Revise a necessidade, a licença e os dois arquivos de dependências antes de
compartilhar a atualização. A lista de ferramentas foi declarada no PDF;
as consultas ao professor sobre TypeScript, documentação e bibliotecas continuam
sendo decisões acadêmicas da equipe, não são comprovadas pela instalação.

## Problemas comuns

| Sintoma                           | Solução                                                              |
| --------------------------------- | -------------------------------------------------------------------- |
| `EBADENGINE`                      | Confira Node 26.x e npm 12.x; reabra o terminal após instalá-los.    |
| Comando não encontrado            | Execute `npm ci` em `frontend`; use os scripts locais.               |
| Porta 3000 ocupada                | Encerre o outro servidor ou use `--port 3001` no desenvolvimento.    |
| Cobertura menor que 80%           | Consulte o relatório e teste os caminhos não exercitados.            |
| TypeDoc acusa referência inválida | Corrija links/docstrings e as entradas configuradas.                 |
| Erro de rede no npm               | Confira conexão, proxy e certificados da sua rede; não desative TLS. |
| `npm start` não encontra a build  | Execute `npm run build` antes de iniciar.                            |

Referências: [Next.js](https://nextjs.org/docs/app/getting-started/installation),
[Vitest](https://vitest.dev/guide/), [TypeScript-ESLint](https://typescript-eslint.io/getting-started/),
[Prettier](https://prettier.io/docs/), [TypeDoc](https://typedoc.org/documents/Options.html).
