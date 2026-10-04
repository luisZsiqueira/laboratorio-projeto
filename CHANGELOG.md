# Changelog

Todas as mudanças relevantes do projeto são registradas neste arquivo.

O formato segue o [Keep a Changelog 1.1.0](https://keepachangelog.com/pt-BR/1.1.0/), e o projeto adota o [Versionamento Semântico 2.0.0](https://semver.org/lang/pt-BR/). Dentro de cada *release*, as mudanças são agrupadas pelo tipo de *commit* do padrão [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/). Os *commits* de *merge* usam a mensagem padrão do git e não são listados.

## [Não publicado]

Nada ainda.

## [0.1.0] - 2026-10-04

Fundação do projeto: regras de trabalho com a IA, documentação, dependências verificadas e arquitetura. Esta *release* não contém código da aplicação; ele começa na `v0.2.0`.

### docs

- Adiciona o README inicial (objetivo, escopo do MVP, prioridades, *stack*, como rodar, roadmap, uso de IA, limitações, créditos e licença) e `docs/requerimentos.md` com os requisitos de entrega do curso (`d55874a`).
- Adiciona `docs/arquitetura.md` com diagramas Mermaid (módulos, fluxo de dados de `POST /tasks` e `GET /health`, modelo de dados) e dez ADRs; reorganiza o roadmap em seis *releases* (`b2dc3f7`).
- Adiciona a licença MIT (`03df816`).
- Adiciona `docs/HISTORY-IA.md`, o histórico do uso de IA generativa por *prompt* (`d255ebe`).
- Registra a publicação no GitHub e a verificação visual dos diagramas Mermaid (`cc4eeed`).
- Registra no `CLAUDE.md` o resultado da checagem de APIs deprecadas, migra o Ponto de partida para o README e define as regras de *merge*, *tag* e `CHANGELOG.md`.
- Adiciona a ADR-11 (`mypy --explicit-package-bases`) e atualiza o comando de checagem de tipos no README e no `CLAUDE.md`.
- Fecha a *release* no README (status, roadmap, uso de IA, solução de problemas do Smart App Control) e adiciona este `CHANGELOG.md`.
- Adiciona `docs/release-review-010.md`, com a revisão de publicação da `v0.1.0`, e registra o Prompt 08.

### build

- Adiciona `requirements.txt` com dependências diretas e transitivas fixadas e verificadas no PyPI em 03/10/2026; adota `httpx2` como cliente do `TestClient` do Starlette 1.7.0 (`2a768bb`).

### chore

- Inicializa o repositório com `.gitignore`, `CLAUDE.md` (regras de trabalho com a IA) e o primeiro *prompt*; os diretórios de `app/` e `tests/` entram no repositório com seus primeiros arquivos (`94f30f2`).
- Amplia o `.gitignore` com seções por tecnologia e corrige o padrão que ignorava o `.env.example` (`c6ca4dd`).

[Não publicado]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/luisZsiqueira/laboratorio-projeto/releases/tag/v0.1.0
