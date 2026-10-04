# Arquitetura

> **Status:** desenho aprovado na *release* `v0.1.0`, antes do código. Serve de *blueprint* para as *releases* `v0.2.0` a `v0.4.0` e será revisado na `v0.5.0`. Divergências da implementação são ajustadas pontualmente no fechamento de cada *release*.

## 1. Visão geral

Micro-API REST síncrona em camadas, com uma camada por pacote em `app/`:

| Camada | Pacote | Responsabilidade | Não pode |
| --- | --- | --- | --- |
| Controller | `app/api/` | rotas HTTP, códigos de resposta, injeção de dependências | acessar o banco ou conter regra de negócio |
| Service | `app/services/` | regras de negócio, incluindo o `priority_advisor` | conhecer HTTP |
| Repository | `app/repositories/` | *engine*, sessão e consultas; único ponto de acesso ao banco | conter regra de negócio |
| Models | `app/models/` | modelos ORM, esquemas Pydantic e configurações | conter lógica |
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
    end

    subgraph services["app/services (regras de negócio)"]
        task_service["task_service.py"]
        priority_advisor["priority_advisor.py"]
        health_service["health_service.py"]
    end

    subgraph repositories["app/repositories (acesso ao banco)"]
        task_repository["task_repository.py"]
        database["database.py<br/>engine, get_db, ping"]
    end

    subgraph models["app/models (estruturas, sem lógica)"]
        task_schemas["task_schemas.py"]
        task["task.py"]
        base["base.py"]
        settings["settings.py"]
    end

    db[("SQLite3")]

    main --> task_routes
    main --> health_routes
    main --> database
    main --> settings

    task_routes --> task_service
    task_routes --> task_schemas
    health_routes --> health_service
    task_routes -.->|"Depends(get_db)"| database
    health_routes -.->|"Depends(get_db)"| database

    task_service --> priority_advisor
    task_service --> task_repository
    task_service --> task_schemas
    health_service --> database

    task_repository --> task
    database --> base
    database --> settings
    task --> base

    database --> db
```

Correspondência com os nomes genéricos: *config* = `settings.py`; *schemas* = `task_schemas.py`; *models* = `task.py` e `base.py`; *repository* = `task_repository.py`; *service* = `task_service.py`; *routes* = `task_routes.py` e `health_routes.py`.

Observações:

- `main.py` importa `database.py` só para criar as tabelas (`Base.metadata.create_all`) no `lifespan`, e `settings.py` para desabilitar a documentação em produção.
- `priority_advisor.py` contém funções puras: não importa repositório, banco nem HTTP.
- `task_schemas.py` define os tipos `TaskStatus` e `TaskPriority` (`typing.Literal`) usados também pelo *service*.

## 3. Fluxo de dados

### POST /tasks

O corpo JSON é validado pelo FastAPI no esquema Pydantic antes de chegar à rota. O *service* recebe o esquema, aplica as regras de prioridade e entrega ao *repository* um objeto ORM, que o grava no SQLite. A resposta volta como objeto ORM e é convertida para o esquema de saída (`from_attributes`) e serializada em JSON.

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant R as task_routes
    participant S as task_service
    participant A as priority_advisor
    participant Rep as task_repository
    participant DB as SQLite3

    C->>R: POST /tasks (JSON)
    Note over C,R: FastAPI converte JSON → TaskCreate (Pydantic)
    alt JSON inválido (título vazio, tamanho, Literal, data/hora)
        R-->>C: 422 Unprocessable Entity
    else válido
        R->>S: create_task(session, TaskCreate)
        S->>A: valida coerência prioridade × due_at
        alt regra violada
            S-->>R: erro de validação de negócio
            R-->>C: 422 Unprocessable Entity
        else coerente
            S->>Rep: add(session, Task ORM)
            Rep->>DB: INSERT (parametrizado pelo ORM)
            DB-->>Rep: linha gravada (id, created_at)
            Rep-->>S: Task (ORM)
            S-->>R: Task (ORM)
            Note over R: response_model converte ORM → TaskRead (Pydantic)
            R-->>C: 201 Created (JSON)
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
    H->>HS: check(session)
    HS->>D: ping(session)
    D->>DB: SELECT 1 via text()
    alt banco responde
        DB-->>D: 1
        D-->>HS: True
        HS-->>H: saudável
        H-->>C: 200 OK (JSON)
    else falha do banco (SQLAlchemyError)
        D-->>HS: False (detalhe registrado no log)
        HS-->>H: indisponível
        H-->>C: 503 Service Unavailable (JSON sem detalhes internos)
    end
```

### Outros códigos de resposta

- **404 Not Found:** `GET`, `PUT`, `PATCH` e `DELETE /tasks/{id}` (e a marcação como concluída) respondem 404 quando o *repository* não encontra a tarefa. O *service* sinaliza com uma exceção de domínio, e a rota a traduz para 404; o *service* não conhece códigos HTTP.
- **500 Internal Server Error:** falha inesperada do banco em operações de tarefa responde com mensagem genérica; o detalhe vai para o log, nunca para o cliente.

## 4. Modelo de dados

Uma única entidade, persistida na tabela `tasks`.

```mermaid
erDiagram
    TASK {
        int id PK "autoincremento"
        string title "obrigatório, 1 a 200 caracteres"
        string description "opcional, até 1000 caracteres"
        string status "TaskStatus (Literal)"
        int priority "TaskPriority (Literal 1 a 4)"
        datetime due_at "opcional, UTC, vazio = tarefa aberta"
        datetime created_at "UTC, definido na criação"
        datetime updated_at "UTC, atualizado a cada alteração"
    }
```

- Tarefa **aberta**: `due_at` vazio. Tarefa **específica**: `due_at` preenchido.
- Prioridades: 1 = mandatória, 2 = importante, 3 = regular, 4 = agendada (na data/hora estipulada).
- Decisões em aberto para o *blueprint* da `v0.3.0`/`v0.4.0`: valores de `TaskStatus` (recomendação: `pending`, `done`); prioridade padrão (recomendação: 3); se prioridade 4 exige `due_at` e vice-versa; filtro por prioridade; regras do `priority_advisor`.

## 5. Decisões de arquitetura

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
| ADR-10 | Datas *timezone-aware* em UTC nos esquemas e na persistência | o SQLite não guarda fuso horário; a conversão para UTC na leitura e na escrita fica na camada de modelos/*repository* e é coberta por testes |
| ADR-11 | Checagem de tipos com `python -m mypy --explicit-package-bases app` | com `app/` sem `__init__.py` (ADR-03), `mypy app` acusa o mesmo arquivo sob dois nomes de módulo (`models.x` e `app.models.x`); a opção faz o mypy derivar o nome do módulo a partir da raiz. Verificado no mypy 2.4.0 em 04/10/2026 |
