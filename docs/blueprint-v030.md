# Blueprint da `v0.3.0`: CRUD de tarefas

> **Status:** proposto para aprovação (Prompt 25, 05/10/2026). Depois de aprovado, é executado pelos Prompts 26 (passo 1), 27 (passo 2), 28 (passo 3), 29 (passo 4), 30 (passo 5) e 31 (passo 6, fechamento). Quem executa lê este arquivo e o `CLAUDE.md`; nada depende do histórico do *chat*.

## 1. Escopo da *release*

| ID | Item | Passo |
| --- | --- | --- |
| RT-05 | Modelo ORM `Task` em `app/models/task.py` | 1 |
| RT-06 | Esquemas Pydantic em `app/models/task_schemas.py` | 1 |
| RT-07 | *Repository* em `app/repositories/task_repository.py` | 2 |
| RT-08 | *Service* em `app/services/task_service.py` e testes unitários | 3 |
| RT-09 | Tratamento de erros (404 e 500) e exemplos de uso no README | 4 e 5 |
| RF-01 a RF-08 | Criar, listar, filtrar por *status*, consultar, atualizar (total e parcial), concluir e excluir | 4 |

Critérios de aceite: os de `docs/backlog.md` (seção 4.2) e os critérios comuns (seção 2). Fluxos: `docs/arquitetura.md`, seção 3 (`POST /tasks` e erros em `/tasks/{id}`). Modelo de dados: seção 4. ADRs aplicados: ADR-01 a ADR-06, ADR-10 a ADR-12, e os novos ADR-14 e ADR-15.

## 2. Decisões tomadas

Não há decisão em aberto neste *blueprint*. As decisões abaixo são confirmadas na aprovação.

### 2.1 Decisões de escopo (D-01 a D-04)

Todas seguem a recomendação de `docs/escopo-mvp.md`, seção 6, sem mudança. São migradas da seção 6 para os requisitos ou ADRs no fechamento (passo 6).

| ID | Decisão |
| --- | --- |
| D-01 | `TaskStatus = Literal["pending", "done"]`; padrão `"pending"` |
| D-02 | Conclusão em `POST /tasks/{task_id}/complete`, idempotente: responde `200` com a tarefa; se ela já estiver `done`, nada é gravado e `updated_at` não muda |
| D-03 | Coluna `priority` criada já nesta *release* (sem migrações, ADR-05); as regras de prioridade ficam na `v0.4.0` |
| D-04 | Prioridade padrão `3` (regular); `TaskPriority = Literal[1, 2, 3, 4]` |

### 2.2 Novos ADRs

Registrados em `docs/arquitetura.md`, seção 6, no passo indicado.

| ID | Decisão | Motivo | Passo |
| --- | --- | --- | --- |
| ADR-14 | O *service* recebe o *repository* por injeção: `TaskService(repository: TaskStore)`, com `TaskStore` (`typing.Protocol`) definido em `task_service.py` e satisfeito estruturalmente por `TaskRepository`. A composição real fica em `build_task_service(session)`, no próprio *service*; a rota só declara `Depends(get_task_service)` | permite os testes unitários do *service* com um dublê simples, sem banco e sem *mock* (CLAUDE.md, Testes); a rota continua sem acesso ao banco | 3 |
| ADR-15 | Contrato dos endpoints de tarefa: rotas e códigos da seção 4; corpo de erro `{"detail": "Tarefa não encontrada"}` no `404` e `{"detail": "Erro interno do servidor"}` no `500`; `422` no formato padrão do FastAPI; campos desconhecidos ou somente leitura (`id`, `created_at`, `updated_at`) na entrada respondem `422` (`extra="forbid"`); `due_at` exige fuso horário (sem fuso: `422`) e é devolvido em UTC com sufixo `Z`; listagem em ordem crescente de `id` | contrato estável e testável; rejeitar em vez de ignorar evita que o cliente pense ter alterado um campo somente leitura | 4 |

### 2.3 Decisões técnicas (DT)

Registradas em `docs/decisoes.md` no mesmo passo do código que as aplica.

| ID | Decisão | Passo |
| --- | --- | --- |
| DT-04 | Tipo de coluna `UTCDateTime` (`TypeDecorator[datetime]`) e função `utc_now()` em `app/models/base.py`: grava em UTC sem fuso, lê com `tzinfo=UTC` e recusa data/hora sem fuso na escrita (`ValueError`). Alternativas descartadas: `DateTime(timezone=True)`, porque o SQLite não guarda fuso e a leitura volta sem `tzinfo`; conversão no *service*, porque deixaria a leitura sem fuso | 1 |
| DT-05 | `TaskPatch` com todos os campos opcionais e `field_validator` que rejeita `null` explícito em `title`, `status` e `priority`; o *service* aplica só `model_dump(exclude_unset=True)`. `description` e `due_at` aceitam `null` para limpar o valor. `PATCH` com corpo `{}` responde `200` sem alterar nada | 1 |
| DT-06 | `created_at` e `updated_at` recebem o mesmo instante na criação, definido pelo *service* com `utc_now()`; nas alterações, `updated_at` muda pelo `onupdate=utc_now` da coluna. Motivo: com dois *defaults* independentes, os valores diferiam em 1 µs no protótipo | 3 |
| DT-07 | Dublê `InMemoryTaskRepository` em `tests/test_task_service.py`: dicionário em memória, `id` sequencial e contador de gravações (`save_count`), usado para provar a idempotência da conclusão | 3 |
| DT-08 | Técnicas dos testes de integração: o `500` é provocado com uma sessão ligada a um banco em memória **sem** a tabela `tasks` (falha real do SQLAlchemy, sem dublê); a mudança de `updated_at` é verificada gravando antes um valor antigo fixo direto no banco (`age_updated_at`), sem depender da resolução do relógio | 4 |

### 2.4 Arquivo novo em relação à estrutura do `CLAUDE.md`

`app/api/error_handlers.py`, dentro de um pacote existente, como a [Estrutura de diretórios](../CLAUDE.md#estrutura-de-diretórios) permite: concentra os tradutores de exceção (404 e 500), que são registrados na aplicação, não em um *router*. Nenhum diretório novo. A estrutura do `CLAUDE.md` é atualizada no fechamento.

## 3. Verificação prévia

O código deste *blueprint* foi executado em protótipo fora do repositório (diretório temporário do assistente), em 05/10/2026, no `.venv` do projeto (Python 3.14.6 e as versões do `requirements.txt`):

- `python -m pytest -W error`: 69 testes passando (13 da `v0.2.0` e 56 novos);
- `python -m mypy --explicit-package-bases app`: sem erros em 17 arquivos;
- `python -m uvicorn app.main:app`: `POST /tasks` com `201` e `due_at` convertido para UTC, `complete`, filtro, `DELETE` com `204` e `404` em seguida, e `/openapi.json` com `200`.

O protótipo revelou dois pontos já incorporados aqui: o `created_at` diferente do `updated_at` na criação (DT-06) e o tipo exigido pelo mypy no parâmetro `responses` das rotas (passo 4).

## 4. Contrato da API

| Método e caminho | Corpo de entrada | Sucesso | Erros |
| --- | --- | --- | --- |
| `POST /tasks` | `TaskCreate` | `201` com `TaskRead` | `422` |
| `GET /tasks?status=` | — (`status` opcional: `pending` ou `done`) | `200` com `list[TaskRead]` | `422` (*status* inválido) |
| `GET /tasks/{task_id}` | — | `200` com `TaskRead` | `404`, `422` (`task_id` não inteiro) |
| `PUT /tasks/{task_id}` | `TaskUpdate` | `200` com `TaskRead` | `404`, `422` |
| `PATCH /tasks/{task_id}` | `TaskPatch` | `200` com `TaskRead` | `404`, `422` |
| `POST /tasks/{task_id}/complete` | — | `200` com `TaskRead` | `404` |
| `DELETE /tasks/{task_id}` | — | `204` sem corpo | `404` |

Qualquer endpoint de tarefa responde `500` com `{"detail": "Erro interno do servidor"}` se o SQLAlchemy falhar; o detalhe vai para o log (logger `app.api.error_handlers`).

## 5. APIs: permitidas e proibidas

### 5.1 Importações permitidas

Usar exatamente estas linhas, por arquivo (estado final de cada arquivo). Nenhuma outra importação de terceiros. Os arquivos da `v0.2.0` não listados aqui não mudam.

```python
# app/models/base.py
from datetime import UTC, datetime
from sqlalchemy import DateTime, Dialect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator

# app/models/task_schemas.py
from datetime import datetime
from typing import Annotated, Literal
from pydantic import AwareDatetime, BaseModel, ConfigDict, StringConstraints, field_validator

# app/models/task.py
from datetime import datetime
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UTCDateTime, utc_now
from app.models.task_schemas import TaskPriority, TaskStatus

# app/repositories/task_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.task_schemas import TaskStatus

# app/services/task_service.py
from collections.abc import Mapping
from typing import Protocol
from sqlalchemy.orm import Session
from app.models.base import utc_now
from app.models.task import Task
from app.models.task_schemas import TaskCreate, TaskPatch, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository

# app/api/error_handlers.py
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.services.task_service import TaskNotFoundError

# app/api/task_routes.py
from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.models.task_schemas import TaskCreate, TaskPatch, TaskRead, TaskStatus, TaskUpdate
from app.repositories.database import get_db
from app.services.task_service import TaskService, build_task_service

# app/main.py (acrescentar às importações existentes)
from app.api.error_handlers import register_error_handlers
from app.api.task_routes import router as task_router

# tests/test_task_service.py
from datetime import UTC
import pytest
from app.models.task import Task
from app.models.task_schemas import TaskCreate, TaskPatch, TaskStatus, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService

# tests/test_task_routes.py (acrescentar às importações existentes; a linha de sqlalchemy é substituída)
from datetime import UTC, datetime, timedelta, timezone
from sqlalchemy import Engine, create_engine, update
from sqlalchemy.exc import StatementError
from app.models.base import Base
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
```

Em `tests/test_task_routes.py`, cada passo acrescenta só as importações que seus testes usam: passo 1, `datetime`/`UTC`/`timedelta`/`timezone`, `StatementError`, `Base` e `Task`; passo 2, `TaskRepository`; passo 4, `update`.

### 5.2 Padrões proibidos

Do roteiro de checagem do `CLAUDE.md` e da rodada desta *release* (verificados em 05/10/2026 nas versões fixadas, com `python -W error`):

| Proibido | Usar | Situação verificada |
| --- | --- | --- |
| `status.HTTP_422_UNPROCESSABLE_ENTITY` | o inteiro `422` nos testes; o código não precisa da constante | `StarletteDeprecationWarning` (Starlette 1.7.0): **novo**, registrar no roteiro do `CLAUDE.md` no passo 1 |
| `session.query(...)` | `session.get(Task, task_id)` e `session.scalars(select(Task)...)` | estilo legado, sem aviso (SQLAlchemy 2.1.3): **novo**, registrar no roteiro no passo 1 |
| `.dict()`, `.from_orm()`, `@validator` | `model_dump()`, `model_validate()` com `from_attributes=True`, `@field_validator` | `PydanticDeprecatedSince20` (Pydantic 2.13.5) |
| `class Config:` | `model_config = ConfigDict(...)` | já no roteiro |
| `datetime.utcnow()` | `utc_now()` de `app/models/base.py` (`datetime.now(UTC)`) | já no roteiro |
| `declarative_base()`, `Column(...)` | `class Base(DeclarativeBase)`, `Mapped[...] = mapped_column(...)` | já no roteiro (estilo legado) |
| `DateTime(timezone=True)` como solução de UTC | `UTCDateTime` (DT-04) | o SQLite devolve sem fuso |
| `Optional[X]` | `X \| None` | convenção do `CLAUDE.md` |

Também proibidos nesta *release*: SQL textual ou montado por concatenação ou *f-string* (só ORM); `Any` e `# type: ignore` em `app/`; `type X = ...` (Python 3.12; o mínimo é 3.11); `__init__.py` em `app/` ou em `tests/`; acesso ao banco nas rotas; importação de FastAPI ou Starlette no *service*; `unittest.mock`.

## 6. Passos

Cada passo termina com a definição de pronto verde, na raiz do repositório, com o `.venv` ativo:

```bash
python -m pytest -W error
python -m mypy --explicit-package-bases app
```

Todas as classes e funções públicas recebem *docstring* em português no formato da `v0.2.0` (propósito; `Args`, `Returns` e `Raises` quando houver).

### Passo 1: tipo UTC, esquemas e modelo `Task` (RT-05, RT-06) — Prompt 26

**Arquivos a alterar:** `app/models/base.py`, `tests/test_task_routes.py`, `docs/decisoes.md` (DT-04 e DT-05), `CLAUDE.md` (duas linhas novas na tabela do roteiro de checagem, conforme 5.2, e o detalhe em `docs/HISTORY-IA.md` no fechamento). **A criar:** `app/models/task_schemas.py`, `app/models/task.py`.

**`app/models/base.py`:** manter `Base` como está e acrescentar `utc_now()` e `UTCDateTime`. Trecho sensível (*docstrings* completas no arquivo):

```python
def utc_now() -> datetime:
    """Devolve o instante atual, timezone-aware, em UTC (ADR-10)."""
    return datetime.now(UTC)


class UTCDateTime(TypeDecorator[datetime]):
    """Coluna de data/hora gravada em UTC e lida como timezone-aware (ADR-10, DT-04)."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("data/hora sem fuso horário não pode ser gravada")
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        if value is None:
            return None
        return value.replace(tzinfo=UTC)
```

**`app/models/task_schemas.py`:**

- `TaskStatus = Literal["pending", "done"]` (D-01); `TaskPriority = Literal[1, 2, 3, 4]` (D-04).
- `TaskTitle = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]`: título só com espaços vira vazio e responde `422`; o título é gravado sem os espaços das pontas.
- `TaskDescription = Annotated[str, StringConstraints(max_length=1000)]`.
- `class TaskCreate(BaseModel)`: `model_config = ConfigDict(extra="forbid")`; campos `title: TaskTitle`, `description: TaskDescription | None = None`, `status: TaskStatus = "pending"`, `priority: TaskPriority = 3`, `due_at: AwareDatetime | None = None`.
- `class TaskUpdate(BaseModel)`: `extra="forbid"`; os mesmos cinco campos, **todos sem padrão** (obrigatórios; `description` e `due_at` aceitam `null`, mas precisam estar presentes).
- `class TaskPatch(BaseModel)`: `extra="forbid"`; os cinco campos opcionais com padrão `None` (`title: TaskTitle | None = None`, `description: TaskDescription | None = None`, `status: TaskStatus | None = None`, `priority: TaskPriority | None = None`, `due_at: AwareDatetime | None = None`) e o validador da DT-05:

```python
    @field_validator("title", "status", "priority")
    @classmethod
    def reject_null(cls, value: object) -> object:
        """Rejeita null explícito nos campos obrigatórios da tarefa (DT-05)."""
        if value is None:
            raise ValueError("o campo não aceita null")
        return value
```

- `class TaskRead(BaseModel)`: `model_config = ConfigDict(from_attributes=True)`; campos `id: int`, `title: str`, `description: str | None`, `status: TaskStatus`, `priority: TaskPriority`, `due_at: datetime | None`, `created_at: datetime`, `updated_at: datetime`.

**`app/models/task.py`:** `class Task(Base)`, `__tablename__ = "tasks"`, sem métodos:

```python
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[TaskStatus] = mapped_column(String(20))
    priority: Mapped[TaskPriority] = mapped_column(Integer)
    due_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime, default=utc_now, onupdate=utc_now
    )
```

O tipo da coluna é sempre explícito (`String`, `Integer`, `UTCDateTime`): o `Literal` da anotação serve ao mypy, e o banco guarda texto e inteiro.

**Testes** (`tests/test_task_routes.py`). Acrescentar a *fixture*:

```python
@pytest.fixture
def task_engine(test_engine: Engine) -> Engine:
    """Engine em memória com as tabelas criadas."""
    Base.metadata.create_all(bind=test_engine)
    return test_engine
```

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_task_dates_are_stored_in_utc_and_read_back_timezone_aware` | numa `Session(task_engine)`, gravar `Task(title="A", description=None, status="pending", priority=3, due_at=datetime(2026, 10, 10, 10, 0, tzinfo=timezone(timedelta(hours=-3))))` e confirmar; reler com `session.get` em outra sessão | `due_at == datetime(2026, 10, 10, 13, 0, tzinfo=UTC)`; `due_at.tzinfo`, `created_at.tzinfo` e `updated_at.tzinfo` são `UTC` |
| `test_task_rejects_naive_datetime_on_write` | `session.add(Task(title="A", status="pending", priority=3, due_at=datetime(2026, 10, 10)))`; `session.commit()` | levanta `StatementError` |

**Verificação:** definição de pronto; 15 testes passando; mypy sem erros.

**IDs:** RT-05 (critérios 1 e 3), RT-06 (critérios 1 a 4), D-01, D-03, D-04, ADR-02, ADR-10, DT-04, DT-05.

### Passo 2: *repository* (RT-07) — Prompt 27

**Arquivo a criar:** `app/repositories/task_repository.py`. **A alterar:** `tests/test_task_routes.py`.

**`class TaskRepository`:** único ponto de acesso à tabela `tasks`; sem regra de negócio; só ORM.

- `__init__(self, session: Session) -> None`: guarda a sessão em `self.session`.
- `add(self, task: Task) -> Task`: `session.add(task)`, `session.commit()`, `session.refresh(task)`; devolve a tarefa (ADR-12).
- `get(self, task_id: int) -> Task | None`: `session.get(Task, task_id)`.
- `find_all(self, status: TaskStatus | None) -> list[Task]`: `select(Task).order_by(Task.id)`, com `.where(Task.status == status)` se `status` não for `None`; devolve `list(session.scalars(statement))`.
- `save(self, task: Task) -> Task`: `session.commit()` e `session.refresh(task)` da tarefa já carregada e alterada; devolve a tarefa.
- `delete(self, task: Task) -> None`: `session.delete(task)` e `session.commit()`.

Exceções do SQLAlchemy não são capturadas aqui: propagam até o tradutor de 500 (passo 4).

**Testes** (`tests/test_task_routes.py`):

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_repository_add_commits_and_refreshes` | `TaskRepository(session).add(Task(title="A", status="pending", priority=3))` numa `Session(task_engine)` | `task.id == 1`; `task.created_at.tzinfo is UTC`; outra `Session(task_engine)` encontra a tarefa com `get(Task, 1)` |
| `test_repository_find_all_filters_by_status_in_id_order` | `add` de `("A", "done")`, `("B", "pending")`, `("C", "done")` | `find_all(None)` → títulos `["A", "B", "C"]`; `find_all("done")` → `["A", "C"]` |

**Verificação:** definição de pronto; 17 testes passando.

**IDs:** RT-07 (critérios 1 a 4), ADR-12, RNF-09.

### Passo 3: *service* e testes unitários (RT-08) — Prompt 28

**Arquivos a criar:** `app/services/task_service.py`, `tests/test_task_service.py`. **A alterar:** `docs/decisoes.md` (DT-06 e DT-07), `docs/arquitetura.md` (ADR-14 na tabela da seção 6).

**`app/services/task_service.py`:**

- `class TaskNotFoundError(Exception)`: `__init__(self, task_id: int) -> None` chama `super().__init__(f"tarefa {task_id} não encontrada")` e guarda `self.task_id`.
- `class TaskStore(Protocol)` (ADR-14) com os métodos `add(self, task: Task) -> Task`, `get(self, task_id: int) -> Task | None`, `find_all(self, status: TaskStatus | None) -> list[Task]`, `save(self, task: Task) -> Task` e `delete(self, task: Task) -> None`, cada um com corpo `...`.
- `class TaskService`, com `__init__(self, repository: TaskStore) -> None` e um método por caso de uso:
  - `create_task(self, task_data: TaskCreate) -> Task`: `created_at = utc_now()`; `Task(**task_data.model_dump(), created_at=created_at, updated_at=created_at)`; devolve `repository.add(task)` (DT-06).
  - `list_tasks(self, status: TaskStatus | None) -> list[Task]`: devolve `repository.find_all(status)`.
  - `get_task(self, task_id: int) -> Task`: devolve a tarefa; se `repository.get` devolver `None`, levanta `TaskNotFoundError(task_id)`.
  - `replace_task(self, task_id: int, task_data: TaskUpdate) -> Task`: `get_task`, `apply_changes(task, task_data.model_dump())`, devolve `repository.save(task)`.
  - `patch_task(self, task_id: int, task_data: TaskPatch) -> Task`: `get_task`, `apply_changes(task, task_data.model_dump(exclude_unset=True))`, devolve `repository.save(task)` (DT-05).
  - `complete_task(self, task_id: int) -> Task`: `get_task`; se `task.status == "done"`, devolve a tarefa **sem** chamar `save`; senão `task.status = "done"` e devolve `repository.save(task)` (D-02).
  - `delete_task(self, task_id: int) -> None`: `repository.delete(self.get_task(task_id))`.
- `def apply_changes(task: Task, changes: Mapping[str, object]) -> None`: `setattr(task, field_name, value)` para cada par de `changes`.
- `def build_task_service(session: Session) -> TaskService`: devolve `TaskService(TaskRepository(session))` (ADR-14).

O módulo não importa FastAPI nem Starlette e não conhece códigos HTTP.

**`tests/test_task_service.py`.** Dublê (DT-07) e *fixtures*:

```python
class InMemoryTaskRepository:
    """Dublê do TaskRepository: guarda as tarefas num dicionário, sem banco (DT-07)."""

    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}
        self.save_count = 0

    def add(self, task: Task) -> Task:
        """Atribui o próximo id e guarda a tarefa."""
        task.id = len(self.tasks) + 1
        self.tasks[task.id] = task
        return task

    def get(self, task_id: int) -> Task | None:
        """Devolve a tarefa guardada ou None."""
        return self.tasks.get(task_id)

    def find_all(self, status: TaskStatus | None) -> list[Task]:
        """Devolve as tarefas por id, filtradas por status se informado."""
        return [
            task
            for task_id, task in sorted(self.tasks.items())
            if status is None or task.status == status
        ]

    def save(self, task: Task) -> Task:
        """Conta a gravação e devolve a tarefa."""
        self.save_count += 1
        return task

    def delete(self, task: Task) -> None:
        """Remove a tarefa."""
        del self.tasks[task.id]


@pytest.fixture
def repository() -> InMemoryTaskRepository:
    """Repositório em memória vazio."""
    return InMemoryTaskRepository()


@pytest.fixture
def service(repository: InMemoryTaskRepository) -> TaskService:
    """Service ligado ao repositório em memória."""
    return TaskService(repository)


def create_sample_task(service: TaskService, title: str = "Estudar FastAPI") -> Task:
    """Cria uma tarefa com os padrões do esquema."""
    return service.create_task(TaskCreate(title=title))
```

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_create_task_applies_schema_defaults` | `create_sample_task(service)` | `id == 1`, `title == "Estudar FastAPI"`, `description is None`, `status == "pending"`, `priority == 3`, `due_at is None`, `created_at == updated_at`, `created_at.tzinfo is UTC` |
| `test_list_tasks_returns_all_without_filter` | criar `"A"` e `"B"`; `list_tasks(None)` | títulos `["A", "B"]` |
| `test_list_tasks_filters_by_status` | criar `"A"`; criar `"B"` e concluí-la | `list_tasks("done")` → `["B"]`; `list_tasks("pending")` → `["A"]` |
| `test_get_task_returns_existing_task` | criar; `get_task(task.id)` | o mesmo objeto (`is`) |
| `test_get_task_raises_when_missing` | `get_task(99)` | `TaskNotFoundError` com `task_id == 99` |
| `test_replace_task_overwrites_all_editable_fields` | criar `TaskCreate(title="A", description="antiga", priority=1)`; `replace_task` com `TaskUpdate(title="B", description=None, status="done", priority=2, due_at=None)` | `("B", None, "done", 2)`; `repository.save_count == 1` |
| `test_replace_task_raises_when_missing` | `replace_task(99, TaskUpdate(...))` com o mesmo corpo | `TaskNotFoundError` |
| `test_patch_task_changes_only_sent_fields` | criar `TaskCreate(title="A", description="mantida", priority=1)`; `patch_task(id, TaskPatch(title="B"))` | `title == "B"`, `description == "mantida"`, `priority == 1`, `status == "pending"` |
| `test_patch_task_raises_when_missing` | `patch_task(99, TaskPatch(title="B"))` | `TaskNotFoundError` |
| `test_complete_task_marks_task_as_done` | criar; `complete_task(id)` | `status == "done"`; `save_count == 1` |
| `test_complete_task_is_idempotent` | criar; `complete_task` duas vezes | `status == "done"`; `save_count == 1` |
| `test_complete_task_raises_when_missing` | `complete_task(99)` | `TaskNotFoundError` |
| `test_delete_task_removes_task` | criar; `delete_task(id)` | `repository.tasks == {}` |
| `test_delete_task_raises_when_missing` | `delete_task(99)` | `TaskNotFoundError` |

**Verificação:** definição de pronto; 31 testes passando (17 + 14).

**IDs:** RT-08 (critérios 1 a 3), D-02, ADR-01, ADR-14, DT-06, DT-07.

### Passo 4: tradutores de erro, rotas e integração (RT-09, RF-01 a RF-08) — Prompt 29

**Arquivos a criar:** `app/api/error_handlers.py`, `app/api/task_routes.py`. **A alterar:** `app/main.py`, `tests/test_task_routes.py`, `docs/decisoes.md` (DT-08), `docs/arquitetura.md` (ADR-15 na tabela da seção 6).

**`app/api/error_handlers.py`.** Trecho sensível (*docstrings* completas no arquivo):

```python
logger = logging.getLogger(__name__)

TASK_NOT_FOUND_DETAIL = "Tarefa não encontrada"
INTERNAL_ERROR_DETAIL = "Erro interno do servidor"


async def handle_task_not_found(request: Request, error: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": TASK_NOT_FOUND_DETAIL}
    )


async def handle_database_error(request: Request, error: Exception) -> JSONResponse:
    logger.error(
        "Falha inesperada do banco de dados em %s %s",
        request.method,
        request.url.path,
        exc_info=error,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": INTERNAL_ERROR_DETAIL},
    )


def register_error_handlers(application: FastAPI) -> None:
    application.add_exception_handler(TaskNotFoundError, handle_task_not_found)
    application.add_exception_handler(SQLAlchemyError, handle_database_error)
```

O parâmetro `error` é tipado como `Exception` (contrato do `add_exception_handler` do Starlette); estreitá-lo quebra o mypy. A resposta nunca inclui a mensagem da exceção.

**`app/api/task_routes.py`:**

- `router = APIRouter(prefix="/tasks", tags=["tasks"])`.
- `NOT_FOUND_RESPONSE: dict[int | str, dict[str, object]] = {status.HTTP_404_NOT_FOUND: {"description": "Tarefa não encontrada"}}`. A anotação é obrigatória: sem ela o mypy recusa o argumento `responses`.
- `def get_task_service(session: Annotated[Session, Depends(get_db)]) -> TaskService`: devolve `build_task_service(session)`.
- `TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]`.
- Rotas síncronas (`def`). Cada uma chama um único método do *service* e converte o resultado com `TaskRead.model_validate(...)` dentro da função, enquanto a sessão está aberta; o tipo de retorno anotado define o esquema da resposta:

| Decorador | Assinatura | Corpo |
| --- | --- | --- |
| `@router.post("", status_code=status.HTTP_201_CREATED)` | `create_task(task_data: TaskCreate, service: TaskServiceDependency) -> TaskRead` | `service.create_task(task_data)` |
| `@router.get("")` | `list_tasks(service: TaskServiceDependency, task_status: Annotated[TaskStatus \| None, Query(alias="status")] = None) -> list[TaskRead]` | `service.list_tasks(task_status)`, convertendo cada item |
| `@router.get("/{task_id}", responses=NOT_FOUND_RESPONSE)` | `read_task(task_id: int, service: TaskServiceDependency) -> TaskRead` | `service.get_task(task_id)` |
| `@router.put("/{task_id}", responses=NOT_FOUND_RESPONSE)` | `replace_task(task_id: int, task_data: TaskUpdate, service: TaskServiceDependency) -> TaskRead` | `service.replace_task(task_id, task_data)` |
| `@router.patch("/{task_id}", responses=NOT_FOUND_RESPONSE)` | `patch_task(task_id: int, task_data: TaskPatch, service: TaskServiceDependency) -> TaskRead` | `service.patch_task(task_id, task_data)` |
| `@router.post("/{task_id}/complete", responses=NOT_FOUND_RESPONSE)` | `complete_task(task_id: int, service: TaskServiceDependency) -> TaskRead` | `service.complete_task(task_id)` |
| `@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE)` | `delete_task(task_id: int, service: TaskServiceDependency) -> None` | `service.delete_task(task_id)` |

O parâmetro de consulta se chama `task_status` com `alias="status"`, para não sombrear o módulo `status` do FastAPI. As rotas não capturam exceções: os tradutores registrados na aplicação fazem isso.

**`app/main.py`:** dentro de `create_app`, depois de `application.include_router(health_router)`, acrescentar `application.include_router(task_router)` e `register_error_handlers(application)`. Nada mais muda. A importação de `task_routes` registra o modelo `Task` no `Base.metadata` (via *service*), e o `create_tables` do `lifespan` passa a criar a tabela `tasks`.

**Testes** (`tests/test_task_routes.py`). Acrescentar os auxiliares (DT-08):

```python
OLD_TIMESTAMP = datetime(2020, 1, 1, tzinfo=UTC)


@pytest.fixture
def broken_db_client(test_engine: Engine) -> Iterator[TestClient]:
    """Cliente cujo get_db usa um banco sem a tabela tasks (falha inesperada real)."""
    engine_without_tables = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    application = create_app(Settings(_env_file=None, environment="test"), test_engine)
    application.dependency_overrides[get_db] = build_get_db_override(
        sessionmaker(bind=engine_without_tables)
    )
    try:
        with TestClient(application) as test_client:
            yield test_client
    finally:
        application.dependency_overrides.clear()
        engine_without_tables.dispose()


def create_task_through_api(client: TestClient, **fields: object) -> dict[str, object]:
    """Cria uma tarefa via POST /tasks e devolve o corpo da resposta."""
    response = client.post("/tasks", json={"title": "Estudar FastAPI", **fields})
    assert response.status_code == 201
    body: dict[str, object] = response.json()
    return body


def age_updated_at(engine: Engine, task_id: object) -> None:
    """Grava um updated_at antigo direto no banco, para comparar depois da alteração."""
    with Session(engine) as session:
        session.execute(update(Task).where(Task.id == task_id).values(updated_at=OLD_TIMESTAMP))
        session.commit()
```

Os testes abaixo usam a *fixture* `client` da `v0.2.0` (banco em memória com as tabelas criadas pelo `lifespan`). `PUT_BODY` abaixo é `{"title": "B", "description": None, "status": "done", "priority": 2, "due_at": None}`.

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_create_task_returns_201_with_generated_fields_and_defaults` | `create_task_through_api(client)` | `id == 1`, `title == "Estudar FastAPI"`, `description`, `due_at` nulos, `status == "pending"`, `priority == 3`, `created_at` termina em `"Z"`, `created_at == updated_at` |
| `test_create_task_converts_due_at_to_utc` | `due_at="2026-10-10T10:00:00-03:00"` | `due_at == "2026-10-10T13:00:00Z"` no `POST` e no `GET /tasks/{id}` seguinte |
| `test_create_task_rejects_invalid_body_with_422` | `@pytest.mark.parametrize("invalid_body", ...)` com 11 corpos: `{"title": ""}`, `{"title": "   "}`, `{"title": "x" * 201}`, `{"title": "A", "description": "x" * 1001}`, `{"title": "A", "status": "archived"}`, `{"title": "A", "priority": 5}`, `{"title": "A", "due_at": "10/10/2026"}`, `{"title": "A", "due_at": "2026-10-10T10:00:00"}`, `{"title": "A", "id": 7}`, `{"title": "A", "created_at": "2026-10-10T10:00:00Z"}`, `{"description": "sem título"}` | `422` em todos |
| `test_create_task_accepts_title_and_description_at_maximum_length` | `title="x" * 200`, `description="y" * 1000` | `201`; título com 200 caracteres |
| `test_list_tasks_returns_empty_list` | `GET /tasks` sem tarefas | `200`; `[]` |
| `test_list_tasks_returns_all_tasks_in_id_order` | criar `"A"` e `"B"` | títulos `["A", "B"]` |
| `test_list_tasks_filters_by_status` | criar `"A"` e `"B"` com `status="done"` | `?status=done` → `["B"]`; `?status=pending` → `["A"]` |
| `test_list_tasks_rejects_invalid_status_with_422` | `GET /tasks?status=archived` | `422` |
| `test_read_task_returns_existing_task` | criar; `GET /tasks/{id}` | `200`; corpo igual ao da criação |
| `test_task_routes_return_404_for_missing_task` | `@pytest.mark.parametrize(("method", "path", "json_body"), ...)` com `("GET", "/tasks/99", None)`, `("PUT", "/tasks/99", PUT_BODY)`, `("PATCH", "/tasks/99", {"title": "B"})`, `("POST", "/tasks/99/complete", None)`, `("DELETE", "/tasks/99", None)`; `client.request(method, path, json=json_body)` | `404`; `json() == {"detail": "Tarefa não encontrada"}` |
| `test_replace_task_overwrites_fields_and_changes_updated_at` | criar com `description="antiga"`, `priority=1`; `age_updated_at(test_engine, id)`; `PUT` com `PUT_BODY` | `200`; `("B", None, "done", 2)`; `created_at` igual ao da criação; `updated_at != "2020-01-01T00:00:00Z"` |
| `test_replace_task_rejects_incomplete_body_with_422` | `PUT` com `{"title": "B"}` | `422` |
| `test_patch_task_changes_only_sent_fields_and_updated_at` | criar com `description="mantida"`, `priority=1`; `age_updated_at`; `PATCH {"title": "B"}` | `200`; `title == "B"`, `description == "mantida"`, `priority == 1`; `updated_at != "2020-01-01T00:00:00Z"` |
| `test_patch_task_clears_nullable_fields` | criar com `description="d"`, `due_at="2026-10-10T10:00:00Z"`; `PATCH {"description": None, "due_at": None}` | `description` e `due_at` nulos |
| `test_patch_task_rejects_invalid_body_with_422` | `parametrize` com `{"title": None}`, `{"status": None}`, `{"priority": None}`, `{"title": ""}`, `{"status": "archived"}`, `{"id": 7}` | `422` em todos |
| `test_complete_task_marks_done_and_is_idempotent` | criar; `POST /complete` duas vezes | ambos `200`; `status == "done"`; segundo corpo igual ao primeiro (inclusive `updated_at`) |
| `test_delete_task_returns_204_and_task_is_gone` | criar; `DELETE` | `204`; `content == b""`; `GET` seguinte `404` |
| `test_task_id_must_be_integer` | `GET /tasks/abc` | `422` |
| `test_database_failure_returns_500_without_internal_details` | *fixture* `broken_db_client`; `with caplog.at_level(logging.ERROR, logger="app.api.error_handlers")`: `GET /tasks` | `500`; `json() == {"detail": "Erro interno do servidor"}`; o texto da resposta não contém `"tasks"` nem `"SELECT"`; `"no such table" in caplog.text` |

**Verificação:** definição de pronto; 69 testes passando (31 + 38 casos, contando cada parâmetro); `git status` sem arquivos novos além dos deste passo (nenhum `tasks.db`).

**IDs:** RT-09 (critérios 1 e 2), RF-01 a RF-08, D-02, ADR-01, ADR-06, ADR-15, DT-08, RNF-08, RNF-10, RNF-11.

### Passo 5: exemplos de uso no README (RT-09, critério 3) — Prompt 30

**Arquivo a alterar:** `README.md`, seção Endpoints (já existe com `GET /health`, desde a `v0.2.0`).

1. Subir a API da raiz com `python -m uvicorn app.main:app --reload`, com `DATABASE_URL` padrão.
2. Executar, nesta ordem e anotando as respostas reais: `POST /tasks` (com `due_at` em `-03:00`), `GET /tasks`, `GET /tasks?status=pending`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `PATCH /tasks/{id}`, `POST /tasks/{id}/complete`, `DELETE /tasks/{id}`, um `404` (`GET /tasks/{id}` depois do `DELETE`) e um `422` (`POST /tasks` com `{"title": ""}`).
3. Na seção Endpoints: tabela única com método, caminho, códigos e descrição (incluindo `/health` e a documentação interativa); para cada endpoint de tarefa, o comando em PowerShell (`Invoke-RestMethod`) e em Bash (`curl`) e o JSON real da resposta; nota sobre UTC, sobre os campos somente leitura e sobre o `500` genérico.
4. Encerrar o servidor. O `tasks.db` da raiz é ignorado pelo `.gitignore`.

Sem alterar código. **Verificação:** definição de pronto (69 testes); `git status` com só o `README.md` alterado neste passo.

**IDs:** RT-09 (critério 3), RNF-13.

### Passo 6: fechamento (Prompt 31)

Arquivos dependentes, conforme "Fechamento de release" e "Arquivos a manter atualizados" do `CLAUDE.md`:

| Arquivo | Atualização |
| --- | --- |
| `README.md` | status; Roadmap com a `v0.3.0` concluída; Endpoints conferida; Uso de IA generativa (modelos dos Prompts 25 a 31); Limitações sem mudança |
| `docs/escopo-mvp.md` | D-01 a D-04 marcadas como decididas na seção 6, com referência a este *blueprint*; seção 2 (`status`) com os valores `pending` e `done` |
| `docs/arquitetura.md` | modelo de dados sem "padrão em aberto" (`status` padrão `pending`, `priority` padrão 3); diagrama de módulos com `error_handlers.py`, `task → task_schemas`, `task_service → base` (`utc_now`) e `main → error_handlers`; diagrama de `POST /tasks` e de erros em `/tasks/{id}` com `create_task(TaskCreate)` sem `session` e `add(Task)` (ADR-14); observação sobre `UTCDateTime` |
| `docs/mermaid.md` | nova seção com o antes e o depois dos diagramas alterados |
| `docs/decisoes.md` | conferir DT-04 a DT-08 |
| `CLAUDE.md` | Estrutura de diretórios com `app/api/error_handlers.py`; roteiro de checagem com as linhas do passo 1 |
| `docs/backlog.md` | RT-05 a RT-09 e RF-01 a RF-08 como `concluído`; horas reais deixadas para o autor |
| `CHANGELOG.md` | seção `0.3.0`, agrupada por tipo de *commit* |
| `docs/HISTORY-IA.md` | entradas dos Prompts 25 a 31 e consolidação da *release*, com a rodada do roteiro de checagem |
| `prompts/Prompt 25` a `Prompt 31` | registro da execução ao final de cada arquivo |

Depois da aprovação do fechamento: *commits* em *Conventional Commits* na *branch* `feat/crud-tarefas`, *merge* `--no-ff` em `main`, *tag* anotada `v0.3.0`, *push* (de `main`, da *tag* e da *branch*) e definição de pronto em clone limpo.

## 7. Riscos

| Risco | Tratamento |
| --- | --- |
| Datas voltarem sem fuso do SQLite ou em outro fuso | `UTCDateTime` (DT-04); testes de persistência (passo 1) e de API com `-03:00` (passo 4) |
| Cliente enviar data/hora sem fuso | `AwareDatetime` responde `422`; o `TypeDecorator` recusa na escrita como segunda barreira |
| `PATCH` gravar `null` em coluna obrigatória (erro 500) | validador da DT-05; teste com `null` em `title`, `status` e `priority` |
| Campos somente leitura aceitos em silêncio | `extra="forbid"` nos três esquemas de entrada; testes com `id` e `created_at` |
| Vazamento de SQL ou nome de tabela no `500` | tradutor devolve texto fixo; detalhe só no log; teste confere a ausência de `tasks` e `SELECT` |
| Teste de `updated_at` instável pela resolução do relógio (Windows com Python 3.11) | `age_updated_at` grava valor antigo fixo antes da alteração (DT-08) |
| *Service* acoplado ao banco nos testes unitários | `TaskStore` (ADR-14) e dublê em memória (DT-07) |
| Rota com regra de negócio ou acesso ao banco | rotas chamam um método do *service* e convertem a resposta; revisão na `v0.5.0` |
| `ResourceWarning` com `-W error` | `engine.dispose()` em `test_engine` e no `broken_db_client`; sessões fechadas pelo `get_db` substituto |
| Testes criarem `tasks.db` | `create_app` com o *engine* em memória (DT-01); conferência de `git status` no passo 4 |
| Literal de configuração fora de `settings.py` | nenhuma configuração nova nesta *release*; mensagens de erro e limites de tamanho são contrato, não configuração |

## 8. O que não fazer

- Não criar `conftest.py`, `pyproject.toml`, `pytest.ini`, `mypy.ini`, `setup.cfg`, `Makefile` nem `.env` versionado; não criar `__init__.py` em `app/` (ADR-03) nem diretórios novos.
- Não criar `app/services/priority_advisor.py` nem `tests/test_priority_advisor.py`, nem regras de coerência entre prioridade e `due_at`: são da `v0.4.0` (RF-09 a RF-11). Nesta *release*, `priority` é só um campo validado pelo `Literal`.
- Não implementar paginação, ordenação configurável, busca, filtro por prioridade (D-06, `v0.4.0`) nem exclusão lógica.
- Não adicionar nem mudar dependências no `requirements.txt`; não importar `httpx` nem `unittest.mock`.
- Não alterar `app/models/settings.py`, `app/models/health_schemas.py`, `app/services/health_service.py`, `app/api/health_routes.py` nem `app/repositories/database.py`; nem os testes da `v0.2.0` (só acrescentar).
- Não capturar exceções nas rotas nem no *repository*; não incluir mensagem de exceção, SQL ou nome de tabela em resposta HTTP.
- Não adicionar `logging.basicConfig` nem configuração de log.
- Não alterar `docs/requerimentos.md`, `docs/PRE-HISTORY-IA.md`, `docs/EXTRA-HISTORY-IA.md`, `docs/release-review-010.md`, `docs/release-prompts-solon-020.md`, `docs/blueprint-v020.md`, `LICENSE` nem `.gitignore`.
- Não comitar sem pedido.

## 9. Condição de parada

Se um passo falhar de forma não prevista (teste, mypy, aviso com `-W error`, importação), ou exigir decisão que este *blueprint* não traz, quem executa para, reporta a saída e não improvisa.

## 10. Estimativa

| Passo | Itens | Horas |
| --- | --- | --- |
| 1 | RT-05, RT-06 | 2 |
| 2 | RT-07 | 0,5 |
| 3 | RT-08 | 1 |
| 4 | RT-09 (critérios 1 e 2), RF-01 a RF-08 | 2,5 |
| 5 | RT-09 (critério 3) | 0,5 |
| **Itens do backlog** | | **6,5** |
| *Blueprint* (este arquivo) e fechamento (passo 6) | fora das estimativas dos itens | 1,5 |
| **Total da *release*** | | **8** |

Os 6,5 h coincidem com o backlog. Somadas à `v0.2.0` (5,5 h previstas com *blueprint* e fechamento), as estimativas seguem dentro do orçamento de cerca de 30 horas; as horas reais são preenchidas pelo autor no backlog.
