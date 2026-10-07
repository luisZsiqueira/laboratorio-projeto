# Arquitetura

> **Status:** desenho aprovado na *release* `v0.1.0`, antes do código, diagramas revisados em 04/10/2026 (Prompt 12) e ajustados à implementação da `v0.2.0` em 05/10/2026 (Prompt 24) da `v0.3.0` em 06/10/2026 (Prompt 31) e da `v0.4.0` em 06/10/2026 (Prompt 35), e revisado na `v0.5.0` em 06/10/2026 (Prompt 37: importações conferidas contra o diagrama de módulos, ADR-19 e ADR-20). Serviu de *blueprint* para as *releases* `v0.2.0` a `v0.4.0`. Divergências da implementação são ajustadas pontualmente no fechamento de cada *release*. O histórico visual dos diagramas (antes e depois de cada revisão) está em [`docs/mermaid.md`](mermaid.md).

## 1. Visão geral

Micro-API REST síncrona em camadas, com uma camada por pacote em `app/`:

| Camada | Pacote | Responsabilidade | Não pode |
| --- | --- | --- | --- |
| Controller | `app/api/` | rotas HTTP, códigos de resposta, injeção de dependências | acessar o banco ou conter regra de negócio |
| Service | `app/services/` | regras de negócio, incluindo o `priority_advisor` | conhecer HTTP |
| Repository | `app/repositories/` | *engine*, sessão e consultas; único ponto de acesso ao banco | conter regra de negócio |
| Models | `app/models/` | modelos ORM, esquemas Pydantic e configurações, incluindo conversões de tipo e de formato (ADR-20) | conter regra de negócio |
| Composição | `app/main.py` | criação da aplicação, `lifespan` e registro das rotas | conter qualquer outra coisa |

Dependências apontam sempre para baixo: Controller → Service → Repository → SQLite3. Os modelos são usados por todas as camadas.

## 2. Módulos e dependências

Cada seta significa "importa". A seta pontilhada indica que as rotas recebem a sessão do banco por `Depends(get_db)` e apenas a repassam ao *service*: **as rotas não fazem consultas**.

```mermaid
flowchart TD
    main["main.py"]

    subgraph api["app/api (controller)"]
        task_routes["task_routes.py"]
        health_routes["health_routes.py"]
        error_handlers["error_handlers.py<br/>404, 422 e 500"]
    end

    subgraph services["app/services (regras de negócio)"]
        task_service["task_service.py"]
        priority_advisor["priority_advisor.py<br/>funções puras"]
        health_service["health_service.py"]
    end

    subgraph repositories["app/repositories (acesso ao banco)"]
        task_repository["task_repository.py"]
        database["database.py<br/>engine, get_db, ping"]
    end

    subgraph models["app/models (estruturas, sem regra de negócio)"]
        task_schemas["task_schemas.py"]
        health_schemas["health_schemas.py"]
        task["task.py"]
        base["base.py<br/>Base, UTCDateTime, utc_now"]
        settings["settings.py"]
    end

    db[("SQLite3")]

    main --> task_routes
    main --> health_routes
    main -->|"create_tables, engine"| database
    main --> settings
    main -->|"register_error_handlers"| error_handlers

    task_routes --> task_service
    task_routes --> task_schemas
    task_routes -->|"Settings"| settings
    health_routes --> health_service
    health_routes --> health_schemas
    task_routes -.->|"Depends(get_db)"| database
    health_routes -.->|"Depends(get_db)"| database
    error_handlers -->|"TaskNotFoundError"| task_service
    error_handlers -->|"IncoherentPriorityError"| priority_advisor

    task_service -->|"ensure_priority_is_coherent, suggest_priority"| priority_advisor
    task_service --> task_repository
    task_service --> task_schemas
    task_service --> task
    task_service -->|"utc_now"| base
    priority_advisor -->|"TaskPriority, TaskStatus"| task_schemas
    health_service --> database
    health_service --> health_schemas

    task_repository --> task
    task_repository -->|"TaskStatus, TaskPriority"| task_schemas
    database --> base
    database --> settings
    task --> base
    task -->|"TaskStatus, TaskPriority"| task_schemas

    database --> db
```

Correspondência com os nomes genéricos: *config* = `settings.py`; *schemas* = `task_schemas.py` e `health_schemas.py`; *models* = `task.py` e `base.py`; *repository* = `task_repository.py`; *service* = `task_service.py`; *routes* = `task_routes.py` e `health_routes.py`.

Observações:

- `main.py` importa de `database.py` só `create_tables` (chamada no `lifespan`, que executa `Base.metadata.create_all`) e o `engine`, e de `settings.py` as configurações que desabilitam a documentação em produção. A aplicação é montada pela fábrica `create_app(settings, db_engine)`, e `app = create_app(get_settings(), engine)` fica no nível do módulo; os testes criam a aplicação com `Settings` e *engine* próprios (DT-01 em [`docs/decisoes.md`](decisoes.md)).
- `health_schemas.py` define `HealthStatus` (`Literal["ok", "unavailable"]`) e o modelo `HealthRead`, devolvido pelo `health_service` e usado como `response_model` pela rota (ADR-13).
- `priority_advisor.py` contém só funções puras (`ensure_priority_is_coherent`, `suggest_priority`) e a exceção `IncoherentPriorityError`; importa apenas `datetime` e os tipos de `task_schemas.py`, não importa banco, *repository* nem HTTP e não lê o relógio: a data/hora de referência é parâmetro (ADR-16). Quem o chama é só o `task_service`; o `error_handlers` importa dele só a exceção.
- `task_schemas.py` define os tipos `TaskStatus` e `TaskPriority` (`typing.Literal`), usados também pelo modelo `Task` (anotações das colunas), pelo *repository* (filtros por *status* e prioridade), pelo *service* e pelo `priority_advisor`. Também define `TaskPriorityQuery`, que aceita o texto da *query string* (DT-12), e `TaskDueAt`, que reconhece os formatos de data local da entrada (DT-13); esses validadores só reconhecem formato, sem regra de negócio.
- `task_service.py` importa `task.py` porque converte o esquema de entrada no objeto ORM `Task` que entrega ao *repository*, e `base.py` pela função `utc_now()`, que dá o mesmo instante a `created_at` e `updated_at` na criação (DT-06). Ele importa `task_repository.py` só em `build_task_service(session, utc_offset)`, a composição usada pela rota; os casos de uso dependem do protocolo `TaskStore` (ADR-14). O *service* recebe também o relógio e o fuso local por injeção (ADR-16, ADR-18), chama o `priority_advisor` e monta a resposta em `build_task_read`, com a sugestão e as datas no fuso local (DT-11).
- `base.py` contém, além do `Base`, o tipo de coluna `UTCDateTime`, que grava as datas em UTC e as devolve *timezone-aware* (DT-04), e a função `utc_now()`.
- `error_handlers.py` traduz `TaskNotFoundError` em `404`, `IncoherentPriorityError` em `422` com texto fixo (ADR-17) e `SQLAlchemyError` em `500` com mensagem genérica (ADR-15); é registrado na aplicação por `main.py`, não em um *router*. Por isso as rotas não capturam exceções.
- `task_routes.py` importa `settings.py` só pelo tipo `Settings`: lê as configurações da aplicação em `request.app.state.settings`, gravadas por `create_app`, para passar `LOCAL_UTC_OFFSET` ao *service* (DT-15).

## 3. Fluxo de dados

### POST /tasks

O corpo JSON é validado pelo FastAPI no esquema Pydantic antes de chegar à rota, incluindo o formato de `due_at` (DT-13). A rota recebe o *service* já composto com o *repository* da sessão e o fuso local (`Depends(get_task_service)`, ADR-14, DT-15). O *service* confere a coerência entre prioridade e prazo no `priority_advisor` (D-05); se ela falhar, a exceção chega ao tradutor de `error_handlers`, que responde `422` com texto fixo (ADR-17). Coerente, o *service* acrescenta o fuso local a um `due_at` digitado sem fuso (ADR-18), converte o esquema num objeto ORM, com `created_at` e `updated_at` no mesmo instante (DT-06), e o entrega ao *repository*, que o grava no SQLite em UTC (DT-04), confirma a transação e recarrega a linha (ADR-12). A rota pede ao *service* a resposta (`build_task_read`, DT-11), que traz a `suggested_priority` calculada pelo `priority_advisor` com o instante do relógio injetado e as datas no fuso local. `PUT` e `PATCH` seguem o mesmo caminho; no `PATCH`, a coerência é conferida no estado resultante (DT-10).

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant R as task_routes
    participant E as error_handlers
    participant S as task_service
    participant A as priority_advisor
    participant Rep as task_repository
    participant DB as SQLite3

    C->>R: POST /tasks (JSON)
    Note over C,R: FastAPI converte JSON → TaskCreate (Pydantic)<br/>due_at em DD/MM/AAAA HH:MM, DD/MM/AAAA (23:59) ou ISO com fuso
    alt JSON inválido (título vazio, tamanho, Literal, formato de due_at, campo extra)
        R-->>C: 422 Unprocessable Content (lista de erros)
    else válido
        R->>S: create_task(TaskCreate)
        S->>A: ensure_priority_is_coherent(priority, due_at)
        alt prioridade 4 sem due_at
            A-->>S: IncoherentPriorityError
            S-->>E: exceção propagada
            E-->>C: 422 {"detail": "Prioridade 4 (agendada) exige due_at preenchido"}
        else coerente
            Note over S: due_at sem fuso recebe o fuso local (LOCAL_UTC_OFFSET)<br/>created_at = updated_at = utc_now()
            S->>Rep: add(Task)
            Rep->>DB: INSERT (parametrizado pelo ORM) + COMMIT
            Rep->>DB: refresh (SELECT da linha gravada)
            DB-->>Rep: id e demais colunas (datas em UTC)
            Rep-->>S: Task (ORM)
            S-->>R: Task (ORM)
            R->>S: build_task_read(Task)
            S->>A: suggest_priority(status, due_at, clock())
            A-->>S: prioridade sugerida ou None
            Note over S: TaskRead com suggested_priority e datas no fuso local
            S-->>R: TaskRead
            R-->>C: 201 Created (JSON, datas no fuso local)
        end
    end
```

### GET /health

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant H as health_routes
    participant HS as health_service
    participant D as database
    participant DB as SQLite3

    C->>H: GET /health
    H->>HS: check_health(session)
    HS->>D: ping(session)
    D->>DB: SELECT 1 via text()
    alt banco responde
        DB-->>D: 1
        D-->>HS: True
        HS-->>H: HealthRead(status="ok", database="ok")
        H-->>C: 200 OK {"status": "ok", "database": "ok"}
    else falha do banco (SQLAlchemyError)
        D-->>HS: False (detalhe registrado no log)
        HS-->>H: HealthRead(status="unavailable", database="unavailable")
        H-->>C: 503 {"status": "unavailable", "database": "unavailable"}
    end
```

### Erros em /tasks/{id}

Vale para `GET`, `PUT`, `PATCH` e `DELETE /tasks/{id}` e para `POST /tasks/{id}/complete`. O corpo inválido, o `id` não numérico e a prioridade incoerente em `PUT` e `PATCH` (422) seguem o fluxo de `POST /tasks`; a existência da tarefa é conferida antes da coerência, então uma tarefa inexistente responde `404`. As rotas não capturam exceções: os tradutores de `app/api/error_handlers.py`, registrados na aplicação, convertem a exceção em resposta HTTP (ADR-15).

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant R as task_routes
    participant E as error_handlers
    participant S as task_service
    participant Rep as task_repository
    participant DB as SQLite3

    C->>R: GET, PUT, PATCH, DELETE /tasks/{id} ou POST /tasks/{id}/complete
    R->>S: operação(id, ...)
    S->>Rep: get(id)
    Rep->>DB: SELECT por id (parametrizado pelo ORM)
    alt tarefa existe
        DB-->>Rep: linha
        Rep-->>S: Task (ORM)
        Note over S,Rep: segue a operação pedida
        S-->>R: resultado
        R-->>C: 200 OK ou 204 No Content
    else tarefa inexistente
        DB-->>Rep: nenhuma linha
        Rep-->>S: None
        S-->>E: TaskNotFoundError(id)
        E-->>C: 404 {"detail": "Tarefa não encontrada"}
    else falha inesperada do banco
        DB-->>Rep: SQLAlchemyError
        Rep-->>S: exceção propagada
        S-->>E: exceção propagada
        Note over E: detalhe registrado no log
        E-->>C: 500 {"detail": "Erro interno do servidor"}
    end
```

- **404 Not Found:** `GET`, `PUT`, `PATCH` e `DELETE /tasks/{id}` e `POST /tasks/{id}/complete` respondem 404 quando o *repository* não encontra a tarefa. O *service* levanta `TaskNotFoundError`, e o tradutor registrado na aplicação a converte em 404, sem o `id` no corpo; o *service* não conhece códigos HTTP.
- **500 Internal Server Error:** falha inesperada do banco (`SQLAlchemyError`) em operações de tarefa responde com mensagem genérica; o detalhe vai para o log (`app.api.error_handlers`), nunca para o cliente.
- **Conclusão idempotente (D-02):** se a tarefa já estiver concluída, o *service* a devolve sem gravar, e `updated_at` não muda.

## 4. Modelo de dados

Uma única entidade, persistida na tabela `tasks`.

```mermaid
erDiagram
    TASK {
        int id PK "autoincremento"
        string title "obrigatório, 1 a 200 caracteres"
        string description "opcional, até 1000 caracteres"
        string status "TaskStatus: pending ou done, padrão pending (D-01)"
        int priority "TaskPriority: 1 a 4, padrão 3 (D-03, D-04), 4 exige due_at (D-05)"
        datetime due_at "opcional, UTC no banco e fuso local na API, vazio = tarefa aberta"
        datetime created_at "UTC no banco e fuso local na API, definido na criação"
        datetime updated_at "UTC no banco e fuso local na API, atualizado a cada alteração"
    }
```

- Atributos e regras conforme [`docs/escopo-mvp.md`](escopo-mvp.md), seção 2.1. O modelo ORM é `Task`, em `app/models/task.py`.
- Tarefa **aberta**: `due_at` vazio. Tarefa **específica**: `due_at` preenchido.
- Prioridades: 1 = mandatória, 2 = importante, 3 = regular, 4 = agendada (na data/hora estipulada). A coluna existe desde a `v0.3.0` (D-03). Prioridade 4 exige `due_at` (D-05). A prioridade sugerida (`suggested_priority`) é calculada a cada resposta e não tem coluna (D-07).
- O padrão de `status` e `priority` é aplicado pelo esquema de entrada (`TaskCreate`), não pela coluna.
- As três colunas de data usam o tipo `UTCDateTime` (DT-04): o SQLite guarda o valor em UTC, sem fuso, e a leitura o devolve com `tzinfo=UTC`. Na gravação, data/hora sem fuso é recusada; na entrada da API, `due_at` em `DD/MM/AAAA HH:MM` ou `DD/MM/AAAA` recebe o fuso local de `LOCAL_UTC_OFFSET` no *service*, e a resposta devolve as datas nesse fuso (ADR-18).

## 5. Testes

Cada arquivo de teste exercita uma parte da aplicação, com o mínimo de infraestrutura. Não há `conftest.py`: cada fixture fica no arquivo que a usa.

```mermaid
flowchart LR
    subgraph tests["tests/"]
        t_service["test_task_service.py<br/>unitários"]
        t_advisor["test_priority_advisor.py<br/>unitários"]
        t_routes["test_task_routes.py<br/>integração"]
    end

    task_service["task_service.py"]
    double["InMemoryTaskRepository<br/>dublê do TaskStore"]
    priority_advisor["priority_advisor.py<br/>funções puras"]
    client["TestClient<br/>(httpx2)"]
    app["aplicação completa<br/>main.py, rotas, services, repositories"]
    persistence["Task e TaskRepository<br/>com Session direta"]
    mem[("SQLite em memória<br/>sqlite:// + StaticPool")]

    t_service --> task_service
    task_service -->|"repository injetado"| double
    t_advisor --> priority_advisor
    t_routes --> client
    client --> app
    app -->|"get_db substituído<br/>(dependency_overrides)"| mem
    t_routes --> persistence
    persistence --> mem
```

- Os unitários não abrem banco nem HTTP. O `priority_advisor` recebe a data/hora de referência como parâmetro, para resultados determinísticos.
- A integração cobre todos os endpoints, incluindo `/health` com banco indisponível e a documentação com `ENVIRONMENT=production`. A fixture chama `engine.dispose()` ao final (ADR-06).
- O `503` de `/health` e o fechamento da sessão em `get_db` são testados com dublês simples de sessão (`FailingSession` e `SessionSpy`), sem biblioteca de *mock* (DT-03 em [`docs/decisoes.md`](decisoes.md)).
- O *service* recebe o dublê `InMemoryTaskRepository` por injeção (ADR-14); o contador `save_count` prova a idempotência da conclusão (DT-07).
- `test_task_routes.py` também testa o modelo `Task` (datas em UTC) e o `TaskRepository` com uma `Session` direta sobre o banco em memória, sem HTTP. O `500` é provocado com um banco em memória sem a tabela `tasks`, e a mudança de `updated_at` é conferida a partir de um valor antigo gravado direto no banco (DT-08).
- Na `v0.4.0` são 134 testes, contando os casos parametrizados: 84 em `test_task_routes.py`, 28 em `test_task_service.py` e 22 em `test_priority_advisor.py`. O *service* dos testes unitários recebe relógio fixo e fuso `-03:00` por injeção (ADR-16, ADR-18).

## 6. Decisões de arquitetura

| # | Decisão | Motivo |
| --- | --- | --- |
| ADR-01 | Camadas Controller → Service → Repository, um pacote por camada | separa HTTP, regra de negócio e persistência; permite testar o *service* com um dublê do *repository* |
| ADR-02 | `Base` declarativo (`class Base(DeclarativeBase)`) em `app/models/base.py`, importado pelos modelos e por `database.py` | evita ciclo de importação entre modelos e *engine* |
| ADR-03 | `app/` sem `__init__.py` na raiz (pacote de *namespace*); comandos executados da raiz via `python -m` | o `python -m` coloca a raiz no `sys.path`, e os testes importam `app` sem `conftest.py` nem arquivo de configuração |
| ADR-04 | SQLite com `connect_args={"check_same_thread": False}` | rotas síncronas rodam no *pool* de *threads* do FastAPI; a sessão é criada e fechada por requisição em `get_db` |
| ADR-05 | Tabelas criadas com `Base.metadata.create_all` no `lifespan` de `app/main.py` | o MVP não tem migrações (Alembic está fora do escopo); `lifespan` substitui o `on_event` legado |
| ADR-06 | Testes com `sqlite://` e `StaticPool`; fixtures chamam `engine.dispose()` | banco em memória compartilhado entre conexões, sem arquivos no repositório e sem aviso de recurso aberto com `-W error` |
| ADR-07 | `/health` segue `health_routes` → `health_service` → `database.ping()`, que executa `SELECT 1` via `text()`; responde 503 se o banco falhar | verificação real do banco, respeitando as camadas; `ping` fica em `database.py` porque não pertence a nenhuma entidade |
| ADR-08 | Documentação interativa (`/docs`, `/redoc`, `/openapi.json`) desabilitada com `ENVIRONMENT=production` | não expor a superfície da API em produção |
| ADR-09 | `httpx2` como cliente HTTP do `TestClient` | o Starlette 1.7.0 o exige; o uso de `httpx` emite aviso de deprecação, que falha com `-W error` |
| ADR-10 | Datas *timezone-aware* em UTC nos esquemas e na persistência (ajustado pelo ADR-18: na API, as datas usam o fuso local) | o SQLite não guarda fuso horário; a conversão para UTC na leitura e na escrita fica na camada de modelos/*repository* e é coberta por testes |
| ADR-11 | Checagem de tipos com `python -m mypy --explicit-package-bases app` | com `app/` sem `__init__.py` (ADR-03), `mypy app` acusa o mesmo arquivo sob dois nomes de módulo (`models.x` e `app.models.x`); a opção faz o mypy derivar o nome do módulo a partir da raiz. Verificado no mypy 2.4.0 em 04/10/2026 |
| ADR-12 | Operações de escrita confirmadas no *repository* (`commit` seguido de `refresh`); `get_db` só abre e fecha a sessão | mantém a persistência num único ponto; o `refresh` devolve os valores gerados pelo banco (`id`, datas); uma sessão fechada sem `commit` descarta alterações pendentes de uma requisição que falhou. Decidido na revisão dos diagramas (Prompt 12), em 04/10/2026 |
| ADR-13 | Contrato de `GET /health` (D-08): modelo `HealthRead` em `app/models/health_schemas.py`, com `status` e `database` do tipo `HealthStatus = Literal["ok", "unavailable"]`. Banco disponível: `200` com `{"status": "ok", "database": "ok"}`; banco indisponível: `503` com `{"status": "unavailable", "database": "unavailable"}` | o corpo não traz mensagem de erro, nome de exceção nem SQL (detalhes só no log, ADR-07); o esquema fica separado dos de tarefa. Decidido no *blueprint* da `v0.2.0` ([`blueprint-v020.md`](blueprint-v020.md)), em 05/10/2026 |
| ADR-14 | O *service* recebe o *repository* por injeção: `TaskService(repository: TaskStore)`, com `TaskStore` (`typing.Protocol`) definido em `task_service.py` e satisfeito estruturalmente por `TaskRepository`. A composição real fica em `build_task_service(session)`, no próprio *service*; a rota só declara `Depends(get_task_service)` | permite os testes unitários do *service* com um dublê simples, sem banco e sem *mock* (`CLAUDE.md`, Testes); a rota continua sem acesso ao banco. Decidido no *blueprint* da `v0.3.0` ([`blueprint-v030.md`](blueprint-v030.md)), em 05/10/2026 |
| ADR-15 | Contrato dos endpoints de tarefa: rotas e códigos de `POST/GET /tasks` e `GET/PUT/PATCH/DELETE /tasks/{task_id}`, mais `POST /tasks/{task_id}/complete` (idempotente, `200`), como em [`blueprint-v030.md`](blueprint-v030.md), seção 4; corpo de erro `{"detail": "Tarefa não encontrada"}` no `404` e `{"detail": "Erro interno do servidor"}` no `500`; `422` no formato padrão do FastAPI; campos desconhecidos ou somente leitura (`id`, `created_at`, `updated_at`) na entrada respondem `422` (`extra="forbid"`); `due_at` exige fuso horário (sem fuso: `422`) e é devolvido em UTC com sufixo `Z` (ajustado pelo ADR-18: devolvido no fuso local); listagem em ordem crescente de `id` | contrato estável e testável; rejeitar em vez de ignorar evita que o cliente pense ter alterado um campo somente leitura; os tradutores de exceção ficam em `app/api/error_handlers.py` e a mensagem de erro nunca traz detalhe interno. Decidido no *blueprint* da `v0.3.0`, em 05/10/2026. Detalhe do contrato: o `PATCH` recusa `null` em `title`, `status` e `priority` (DT-05) |
| ADR-16 | `app/services/priority_advisor.py` contém só funções puras e a exceção `IncoherentPriorityError`; importa apenas `datetime` e os tipos de `task_schemas.py`. Não importa banco, *repository*, FastAPI nem Starlette e não lê o relógio: a data/hora de referência é parâmetro. O instante atual vem do relógio injetado no *service*: `TaskService(repository: TaskStore, clock: Callable[[], datetime] = utc_now)`. Quem chama o *advisor* é só o `task_service` | regras determinísticas e testáveis sem banco, sem HTTP e sem depender do instante da execução (RNF-03); o *service* continua o único ponto de regra de negócio (ADR-01). Decidido no *blueprint* da `v0.4.0` ([`blueprint-v040.md`](blueprint-v040.md)), em 06/10/2026 |
| ADR-17 | Contrato da `v0.4.0`, somado ao ADR-15: `TaskRead` ganha `suggested_priority` (`TaskPriority` ou `null`), calculado a cada resposta e nunca gravado (D-07); combinação incoerente (D-05) responde `422` com `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`, no formato dos outros erros de domínio (`404`, `500`) e não no formato de lista da validação do FastAPI; `GET /tasks` aceita `?priority=` (1 a 4), combinável com `?status=` (RF-14) | mensagem única e clara para a regra de negócio; o cliente distingue erro de forma (lista) de erro de regra (texto); a prioridade gravada continua sendo a escolha do usuário. Decidido no *blueprint* da `v0.4.0`, em 06/10/2026. A resposta é montada no *service* por `build_task_read` (DT-11) |
| ADR-18 | Horário local na fronteira da API (D-09), ajustando o ADR-10 e o ADR-15: o banco continua em UTC; a entrada aceita `DD/MM/AAAA HH:MM` e `DD/MM/AAAA` (23:59) no fuso local, além de ISO 8601 com fuso; as respostas trazem as datas no fuso local. O fuso é o deslocamento fixo de `LOCAL_UTC_OFFSET` (`Settings`), passado ao *service* (`TaskService(..., local_timezone=...)`), que acrescenta o fuso às datas locais da entrada e converte as datas da resposta em `build_task_read`. A rota obtém as `Settings` da aplicação em `request.app.state.settings`, gravadas por `create_app` | formato fácil de digitar e de ler; a conversão fica num único ponto (o *service*), sem regra nos esquemas além do reconhecimento do formato; a persistência em UTC (DT-04) não muda, e o ISO com fuso continua aceito para quem já usa a API. Decidido no *blueprint* da `v0.4.0`, em 06/10/2026 |
| ADR-19 | Composição da aplicação pela fábrica `create_app(settings, db_engine)` em `app/main.py`, que cria a aplicação, registra rotas e tradutores e grava as `Settings` em `application.state.settings`; as rotas leem as configurações de `request.app.state.settings` para compor o *service*. O módulo expõe `app = create_app(get_settings(), engine)` para o uvicorn | os testes criam aplicações com `Settings` e *engine* próprios, sem depender do ambiente nem do `.env` da máquina; as rotas não leem o ambiente. Promove a DT-01 e a DT-15 na revisão da `v0.5.0` ([`blueprint-v050.md`](blueprint-v050.md)), em 06/10/2026 |
| ADR-20 | `app/models/` contém estruturas e também conversões de tipo e de formato, sem regra de negócio: o tipo de coluna `UTCDateTime` (DT-04) e os validadores de formato dos esquemas, `convert_priority_text` (DT-12) e `parse_local_due_at` (DT-13). Regra de negócio (coerência, sugestão, fuso local da entrada) fica só em `app/services/` (ADR-01, ADR-16, ADR-18) | a conversão para UTC precisa estar no tipo de coluna para valer em toda gravação e leitura; o reconhecimento do formato precisa estar no esquema para que entrada mal formada responda `422` antes da rota. Ajusta a regra "modelos sem lógica" do ADR-01 e do `CLAUDE.md`. Promove a DT-04, a DT-12 e a DT-13 na revisão da `v0.5.0`, em 06/10/2026 |
