# Changelog

Todas as mudanças relevantes do projeto são registradas neste arquivo.

O formato segue o [Keep a Changelog 1.1.0](https://keepachangelog.com/pt-BR/1.1.0/), e o projeto adota o [Versionamento Semântico 2.0.0](https://semver.org/lang/pt-BR/). Dentro de cada *release*, as mudanças são agrupadas pelo tipo de *commit* do padrão [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/). Os *commits* de *merge* usam a mensagem padrão do git e não são listados.

## [Não publicado]

## [1.0.0] - 2026-10-07

Entrega do curso, sem mudança de código nem de dependências, executada a partir de [`docs/blueprint-v100.md`](docs/blueprint-v100.md): validação em máquina limpa, histórico de uso de IA consolidado e publicação. O comportamento da API é o da `v0.5.0`; são 143 testes, que passam com `python -m pytest -W error`.

### docs

- Adiciona `docs/blueprint-v100.md`, o *blueprint* da *release*, com o levantamento prévio, as decisões E-01 a E-15, o roteiro de validação, a lista de verificação do histórico e o checklist dos requisitos do curso.
- Valida a instalação, a execução, os exemplos da seção Endpoints e os testes em clone limpo, só com os comandos do README, em PowerShell e em Git Bash (RT-15). O README ganha a ativação do `.venv` no Git Bash do Windows (`source .venv/Scripts/activate`) e a forma Bash da Solução de problemas do SQLAlchemy; Linux/macOS fica registrado como não verificado.
- Consolida o histórico de uso de IA em `docs/HISTORY-IA.md` (RT-16): entradas dos Prompts 41 a 44, consolidação do intervalo entre a `v0.1.0` e a `v0.2.0` e da `v1.0.0`, tabela Ambiente com o modelo de cada *prompt*, motivo da numeração dos *prompts* e análise final (uso por modelo, ganho percebido e horas reais, desafios, decisões que ficaram com o humano e lições).
- Atualiza o README (Uso de IA generativa) com todos os assistentes, modelos e etapas, inclusive o Claude in Chrome nos Prompts 31 e 35 e a `v1.0.0`; corrige o *link* local de `docs/EXTRA-HISTORY-IA.md`; marca `prompts/prompts-desenvolvimento.md` como executado, com a nota sobre o mypy (ADR-21).
- Registra nos Prompts 41 e 42 os *commits* feitos na sessão do Prompt 42, conferidos no `git log`.
- Fecha a *release* (RT-17): README com status "concluído" e o roadmap com todas as *releases* concluídas; rastreabilidade com os requisitos do curso toda como atendida em `docs/escopo-mvp.md`; RT-15 a RT-17 concluídos em `docs/backlog.md`, com 2 h reais na `v1.0.0` e 21 h no total, da `v0.2.0` à `v1.0.0`; status do *blueprint*.

## [0.5.0] - 2026-10-07

Revisão de arquitetura, segurança, dependências e documentação, sem funcionalidade nova, executada a partir de [`docs/blueprint-v050.md`](docs/blueprint-v050.md). Inclui também o registro do fechamento da `v0.4.0`, feito em `main` depois da *tag*.

**Mudança de comportamento:** um `id` acima de `9223372036854775807` nas rotas de `/tasks/{id}` passa a responder `422`, e não mais `500`.

### fix

- Limita `task_id` ao maior `INTEGER` do SQLite (`2**63 - 1`) com o tipo `TaskId`: acima disso, as rotas de `/tasks/{task_id}` respondiam `500` não tratado (`OverflowError` do driver) e passam a responder `422` (RT-12, RNF-08, DT-16).
- Cria o engine com `hide_parameters=True`: o log da falha do banco deixa de trazer os valores enviados pelo cliente (título, descrição); o SQL e o erro continuam no log (RT-12, RNF-10, DT-17).

### build

- Remove o mypy 2.4.0 do `requirements.txt`, com as dependências transitivas que só ele usava (`librt`, `ast_serialize`, `mypy_extensions` e `pathspec`): o Smart App Control do Windows bloqueia as suas extensões compiladas. A definição de pronto passa a ser só `python -m pytest -W error`, e a tipagem é conferida na revisão de código (ADR-21, que substitui o ADR-11).

### test

- Adiciona a `tests/test_task_routes.py` `test_task_id_above_integer_limit_has_no_internal_details` (5 casos, um por rota), `test_validation_errors_have_no_internal_details` (3 casos: formato de `due_at`, prioridade fora do `Literal` e JSON malformado) e `test_database_failure_log_has_no_request_values`; são 143 testes no total.

### docs

- Registra o resultado do fechamento da `v0.4.0` no Prompt 35 e em `docs/HISTORY-IA.md`: *commits*, *merge*, *tag*, *push*, clone limpo e renderização dos diagramas no GitHub.
- Adiciona `docs/blueprint-v050.md`: ordem das revisões, forma do checklist, regra de decisão entre código e documento e critério de promoção de DT a ADR (R-01 a R-07).
- Revisa a arquitetura (RT-11): importações conferidas contra o diagrama de módulos, sem desvio de código; ADR-19 (composição por `create_app`, promove DT-01 e DT-15) e ADR-20 (conversões de formato em `app/models/`, promove DT-04, DT-12 e DT-13); citações nos ADR-15 e ADR-17; diagrama de módulos com o antes e o depois em `docs/mermaid.md`.
- Revisa a documentação e as dependências (RT-13, RT-14): exemplos do README executados de novo na API, sem divergência; versões conferidas no PyPI em 07/10/2026, sem mudança; `docs/arquitetura.md` com `TaskId` (DT-16), `hide_parameters` (DT-17), a contagem de 143 testes e a assinatura de `build_task_service` ajustada pelo ADR-18; `docs/escopo-mvp.md` com a origem da D-08.
- Fecha a `v0.5.0`: README (status, roadmap, Uso de IA generativa e limitações, com o nome do validador no `422` de formato pela R-05 e a ausência de checagem de tipos por ferramenta), backlog (RT-11 a RT-14 concluídos, 4 h reais), escopo, `docs/arquitetura.md`, status do *blueprint* e `docs/HISTORY-IA.md` (Prompts 39 e 40 e consolidação); `CLAUDE.md` alinhado ao ADR-20 (`app/models/` com conversões de formato, sem regra de negócio), à promoção de DTs feita na revisão, ao `422` de coerência em `error_handlers.py` e ao `TaskId`.

## [0.4.0] - 2026-10-06

Prioridades e `priority_advisor`: coerência entre prioridade e prazo, prioridade sugerida pela proximidade do prazo, filtro por prioridade e datas no horário local. Código executado a partir de [`docs/blueprint-v040.md`](docs/blueprint-v040.md). Inclui também as mudanças de documentação feitas em `main` depois da `v0.3.0`.

**Mudança de contrato:** as datas da resposta (`due_at`, `created_at`, `updated_at`) passam a vir no fuso local de `LOCAL_UTC_OFFSET` (padrão `-03:00`), e não mais em UTC com sufixo `Z`; o ISO 8601 com fuso continua aceito na entrada (ADR-18).

### feat

- Adiciona `app/services/priority_advisor.py`, só com funções puras: `ensure_priority_is_coherent` (prioridade 4 exige `due_at`) e `suggest_priority` (por faixas de 4 h, 24 h e 7 dias, com a data/hora de referência como parâmetro), e a exceção `IncoherentPriorityError` (RT-10, D-05, D-07, ADR-16, DT-09).
- Integra o *advisor* ao `TaskService`: coerência na criação, no `PUT` e no `PATCH` (no estado resultante, antes de alterar a tarefa) e resposta montada por `build_task_read`, com `suggested_priority` calculada com o relógio injetado e nunca gravada (RF-10, RF-11, DT-10, DT-11).
- Traduz `IncoherentPriorityError` em `422` com `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}` em `app/api/error_handlers.py` (ADR-17).
- Adiciona o filtro `GET /tasks?priority=1` a `4`, combinável com `?status=`, com `TaskPriorityQuery` para aceitar o texto da *query string* (RF-14, D-06, DT-12).
- Aceita `due_at` em `DD/MM/AAAA HH:MM` e `DD/MM/AAAA` (até 23:59) no horário local, além de ISO 8601 com fuso, e devolve as datas no fuso local; nova variável `LOCAL_UTC_OFFSET` (`±HH:MM`, padrão `-03:00`) (RF-09, D-09, ADR-18, DT-13 a DT-15).
- Adiciona `tests/test_priority_advisor.py` (22 casos) e 43 casos em `tests/test_task_service.py` e `tests/test_task_routes.py`; ajusta os testes da `v0.3.0` afetados pelas datas no fuso local; são 134 testes no total.

### docs

- Adiciona `docs/blueprint-v040.md`, o *blueprint* executável da *release*, com D-05 a D-07 e D-09, os ADR-16 a ADR-18 e as DT-09 a DT-15.
- Adiciona os ADR-16 a ADR-18 em `docs/arquitetura.md` (com a observação de ajuste nos ADR-10 e ADR-15) e as DT-09 a DT-15 em `docs/decisoes.md`.
- Atualiza no `CLAUDE.md` a linha de `HTTP_422_UNPROCESSABLE_ENTITY` do roteiro de checagem (`HTTP_422_UNPROCESSABLE_CONTENT` permitido) e a convenção de datas (UTC na persistência, fuso local na API).
- Ajusta à implementação os diagramas de módulos, de `POST /tasks` e do modelo de dados, e registra o antes e o depois em `docs/mermaid.md`.
- Incorpora D-05 a D-07 e D-09 aos requisitos de `docs/escopo-mvp.md`, inclui o RF-14 e atualiza a rastreabilidade com os requisitos do curso.
- Revisa o README: status, escopo, prioridades com a tabela de sugestão, Endpoints (filtro, `suggested_priority`, formatos de `due_at`, `422` de coerência) com exemplos executados na API, Configuração com `LOCAL_UTC_OFFSET`, roadmap, Uso de IA generativa e limitações.
- Marca RT-10, RF-09 a RF-11 e RF-14 como concluídos em `docs/backlog.md`, com o critério 3 do RF-09 substituído pelos da D-09.
- Registra os Prompts 32 a 35 em `prompts/` e em `docs/HISTORY-IA.md`, com a consolidação da *release*.
- Registra o resultado do fechamento da `v0.3.0` no Prompt 31 e em `docs/HISTORY-IA.md`: *commits*, *merge*, *tag*, *push*, clone limpo e renderização dos diagramas no GitHub.
- Registra em `docs/backlog.md` as horas reais informadas pelo autor: 4 h para a `v0.2.0` e 8 h para a `v0.3.0`.

## [0.3.0] - 2026-10-06

CRUD de tarefas: criar, listar com filtro por *status*, consultar, atualizar (total e parcial), concluir e excluir, com datas em UTC e erros sem detalhes internos. Código executado a partir de [`docs/blueprint-v030.md`](docs/blueprint-v030.md). Inclui também as mudanças de documentação feitas em `main` depois da `v0.2.0`.

### feat

- Adiciona o modelo ORM `Task` em `app/models/task.py` e, em `app/models/base.py`, o tipo de coluna `UTCDateTime` e a função `utc_now()`: datas gravadas em UTC e lidas *timezone-aware*, com recusa de data/hora sem fuso (RT-05, DT-04).
- Adiciona os esquemas `TaskCreate`, `TaskUpdate`, `TaskPatch` e `TaskRead` e os tipos `TaskStatus` (`pending`, `done`) e `TaskPriority` (1 a 4) em `app/models/task_schemas.py`; campos desconhecidos ou somente leitura respondem `422`, e `PATCH` rejeita `null` em `title`, `status` e `priority` (RT-06, D-01, D-04, DT-05).
- Adiciona `app/repositories/task_repository.py`, só com ORM e escritas confirmadas com `commit` e `refresh` (RT-07, ADR-12).
- Adiciona `app/services/task_service.py` com os casos de uso, a exceção `TaskNotFoundError` e o *repository* injetado pelo protocolo `TaskStore`; a conclusão é idempotente (RT-08, D-02, ADR-14, DT-06).
- Adiciona as rotas de `/tasks` em `app/api/task_routes.py` e os tradutores de `404` e `500` em `app/api/error_handlers.py`, registrados em `app/main.py` (RF-01 a RF-08, RT-09, ADR-15).
- Adiciona `tests/test_task_service.py` (14 testes unitários com o dublê `InMemoryTaskRepository`, DT-07) e 42 casos de teste em `tests/test_task_routes.py` (modelo, *repository* e integração dos endpoints, incluindo `404`, `422` e `500`, DT-08); são 69 testes no total.

### docs

- Adiciona `docs/blueprint-v030.md`, o *blueprint* executável da *release*, com D-01 a D-04, os ADR-14 e ADR-15 e as DT-04 a DT-08.
- Adiciona os ADR-14 e ADR-15 em `docs/arquitetura.md` e as DT-04 a DT-08 em `docs/decisoes.md`; ordena as DTs pelo número.
- Registra no roteiro de checagem do `CLAUDE.md` `status.HTTP_422_UNPROCESSABLE_ENTITY` (proibido) e `session.query` (estilo legado); inclui `error_handlers.py` na estrutura de diretórios.
- Ajusta à implementação os diagramas de módulos, de `POST /tasks`, de erros em `/tasks/{id}`, do modelo de dados e dos testes, e registra o antes e o depois em `docs/mermaid.md`.
- Incorpora as decisões D-01 a D-04 aos requisitos de `docs/escopo-mvp.md` e atualiza a rastreabilidade com os requisitos do curso.
- Reescreve a seção Endpoints do README, com a tabela de endpoints, os campos da tarefa, os erros e exemplos executados na API em PowerShell e Bash; revisa o status, o roadmap e o Uso de IA generativa.
- Marca RT-05 a RT-09 e RF-01 a RF-08 como concluídos em `docs/backlog.md`.
- Registra os Prompts 25 a 31 em `prompts/` e em `docs/HISTORY-IA.md`, com a consolidação da *release*.
- Registra o resultado do fechamento da `v0.2.0` (*commits*, *merge*, *tag*, *push* e clone limpo) no Prompt 24 e em `docs/HISTORY-IA.md`.
- Identifica o modelo do Prompt 21 (Claude Opus 5.5) no arquivo do *prompt*, no histórico e no README.
- Registra a validação de sintaxe dos diagramas alterados pelo serviço mermaid.ink e deixa as horas reais da `v0.2.0` para preenchimento do autor no backlog.

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

[Não publicado]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.5.0...v1.0.0
[0.5.0]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/luisZsiqueira/laboratorio-projeto/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/luisZsiqueira/laboratorio-projeto/releases/tag/v0.1.0
