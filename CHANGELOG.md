# Changelog

Todas as mudanças relevantes do projeto são registradas neste arquivo.

O formato segue o [Keep a Changelog 1.1.0](https://keepachangelog.com/pt-BR/1.1.0/), e o projeto adota o [Versionamento Semântico 2.0.0](https://semver.org/lang/pt-BR/). Dentro de cada *release*, as mudanças são agrupadas pelo tipo de *commit* do padrão [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/). Os *commits* de *merge* usam a mensagem padrão do git e não são listados.

## [Não publicado]

## [0.2.0] - 2026-10-05

Base técnica: configuração por ambiente, acesso ao banco SQLite, aplicação FastAPI com `lifespan`, `GET /health` e infraestrutura de testes de integração. Primeiro código da aplicação, executado a partir de [`docs/blueprint-v020.md`](docs/blueprint-v020.md). Inclui também as mudanças de documentação feitas em `main` depois da `v0.1.0`.

### feat

- Adiciona `app/models/settings.py` com `Settings` (pydantic-settings, `SettingsConfigDict`), `DATABASE_URL` e `ENVIRONMENT` tipada com `Literal`, e `get_settings()` com `lru_cache` (RT-01, DT-02).
- Adiciona `app/models/base.py` (`class Base(DeclarativeBase)`) e `app/repositories/database.py` com *engine*, `SessionLocal`, `get_db`, `create_tables` e `ping` (`SELECT 1` via `text()`, falha registrada só no log) (RT-02).
- Adiciona `GET /health` em camadas: `app/models/health_schemas.py` (`HealthRead`, D-08 e ADR-13), `app/services/health_service.py` (`check_health`) e `app/api/health_routes.py`; responde `200` ou `503` sem detalhes internos (RF-12).
- Adiciona `app/main.py` com a fábrica `create_app(settings, db_engine)`, `lifespan` com `@asynccontextmanager` que cria as tabelas, e documentação interativa desabilitada com `ENVIRONMENT=production` (RT-03, RF-13, DT-01).
- Adiciona `tests/test_task_routes.py` com 13 testes: configuração, `get_db`, `ping`, `lifespan`, `/health` 200 e 503 e documentação por ambiente; SQLite em memória com `StaticPool`, `engine.dispose()` e dublês de sessão sem biblioteca de *mock* (RT-04, DT-03).

### docs

- Adiciona `docs/blueprint-v020.md`, o *blueprint* executável da *release*, e `docs/decisoes.md` com as decisões técnicas DT-01 a DT-03.
- Adiciona o ADR-13 (contrato de `GET /health`) em `docs/arquitetura.md` e marca a D-08 como decidida em `docs/escopo-mvp.md`.
- Ajusta os diagramas de módulos e de `GET /health` à implementação e registra o antes e o depois em `docs/mermaid.md`.
- Revisa o README: status, seção Endpoints com `GET /health`, Configuração, Como rodar, roadmap com a `v0.2.0` concluída e Uso de IA generativa.
- Marca RT-01 a RT-04, RF-12 e RF-13 como concluídos em `docs/backlog.md`.
- Remove do `CLAUDE.md` a seção Ponto de partida, já migrada, e inclui `health_schemas.py` na estrutura de diretórios.
- Registra os Prompts 21 a 24 em `prompts/` e em `docs/HISTORY-IA.md`, com a consolidação da *release*.
- Adiciona `docs/escopo-mvp.md` com objetivo, critérios de sucesso, requisitos funcionais (RF-01 a RF-13) e não funcionais (RNF-01 a RNF-15), fora de escopo, decisões em aberto e rastreabilidade com os requisitos do curso.
- Torna `docs/escopo-mvp.md` a fonte de verdade dos requisitos no `CLAUDE.md` e migra para ele as decisões em aberto do Ponto de partida e de `docs/arquitetura.md`; o README passa a apontar para o documento.
- Registra o Prompt 10 no histórico de uso de IA.
- Adiciona `docs/backlog.md` com os itens das *releases* `v0.2.0` a `v1.0.0`: 13 requisitos funcionais (RF) e 17 técnicos (RT), critérios de aceite verificáveis, estimativas e rastreabilidade com os requisitos não funcionais.
- Inclui o backlog nas fontes de verdade, na estrutura e nas regras de fechamento de *release* do `CLAUDE.md`, e o referencia no README e no escopo; registra o Prompt 11.
- Revisa os diagramas Mermaid de `docs/arquitetura.md`: acrescenta a dependência `task_service → task`, o `commit` e o `refresh` no fluxo de `POST /tasks` (ADR-12), os padrões em aberto no modelo de dados e dois diagramas novos (erros em `/tasks/{id}` e testes).
- Adiciona `docs/mermaid.md`, catálogo dos diagramas com o antes e o depois da revisão; registra a decisão D-08 (esquema de `/health`) no escopo e no backlog; registra o Prompt 12.
- Adiciona `docs/PRE-HISTORY-IA.md`, com o uso de IA anterior ao repositório: concepção do `CLAUDE.md` no Claude em modo *chat*, em 01 e 02/10/2026.
- Acrescenta ao `CLAUDE.md` as regras de nomenclatura semântica, funções coesas e tipagem, o registro de decisões técnicas em `docs/decisoes.md` (DT) e a regra de *blueprint* executável por outro modelo, gravado em `docs/blueprint-vXYZ.md`.
- Atualiza o README (Uso de IA generativa) e o `HISTORY-IA.md`; registra o Prompt 13.
- Adiciona `prompts/prompts-desenvolvimento.md`, com os 24 *prompts* (21 a 44) da fase de desenvolvimento, das *releases* `v0.2.0` a `v1.0.0`, adaptados do exemplo do tutor em `docs/release-prompts-solon-020.md`; adiciona `docs/EXTRA-HISTORY-IA.md` (uso de IA em modo *chat* fora do repositório) e registra os três arquivos no `CLAUDE.md` e no README; registra o Prompt 20.

### chore

- Renomeia `prompts/Prompt00 - Inicio` para `prompts/Prompt 00 - criar diretorios e main`, no padrão dos demais *prompts*.

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

[Não publicado]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/luisZsiqueira/laboratorio-projeto/releases/tag/v0.1.0
