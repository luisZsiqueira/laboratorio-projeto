# Blueprint da `v0.2.0`: base técnica

> **Status:** aprovado e executado. Proposto no Prompt 21 (05/10/2026) e executado pelos Prompts 22 (passos 1 e 2), 23 (passos 3 a 5) e 24 (passo 6, fechamento), sem divergência de código. Quem executa lê este arquivo e o `CLAUDE.md`; nada depende do histórico do *chat*.

## 1. Escopo da *release*

| ID | Item | Passo |
| --- | --- | --- |
| RT-01 | Configuração por ambiente em `app/models/settings.py` | 1 |
| RT-02 | Base declarativa e acesso ao banco (`base.py`, `database.py`) | 2 |
| RF-12 | `GET /health` | 3 e 4 |
| RT-03 | Composição da aplicação em `app/main.py` | 4 |
| RT-04 | Infraestrutura de testes de integração em `tests/test_task_routes.py` | 1, 2 e 4 |
| RF-13 | Documentação interativa conforme o ambiente | 4 |

Critérios de aceite: os de `docs/backlog.md` (seção 4.1) e os critérios comuns (seção 2). Fluxo de `/health`: `docs/arquitetura.md`, seção 3. ADRs aplicados: ADR-02 a ADR-09 e ADR-11.

## 2. Decisões tomadas

Não há decisão em aberto neste *blueprint*. As decisões abaixo são confirmadas na aprovação.

| ID | Decisão | Onde é registrada | Passo |
| --- | --- | --- | --- |
| D-08 | Esquema da resposta de `/health` em novo arquivo `app/models/health_schemas.py`: modelo `HealthRead` com os campos `status` e `database`, ambos do tipo `HealthStatus = Literal["ok", "unavailable"]`. Banco disponível: `200` com `{"status": "ok", "database": "ok"}`. Banco indisponível: `503` com `{"status": "unavailable", "database": "unavailable"}`. Recomendação do escopo, sem mudança | `docs/escopo-mvp.md` (D-08 marcada como decidida) e ADR-13 em `docs/arquitetura.md` (contrato da API) | 3 |
| DT-01 | `app/main.py` expõe a fábrica `create_app(settings, db_engine)` e cria `app = create_app(get_settings(), engine)` no nível do módulo. Os testes criam a aplicação com `Settings` e *engine* próprios | `docs/decisoes.md` (arquivo criado neste passo) | 4 |
| DT-02 | `get_settings()` com `functools.lru_cache(maxsize=1)`: uma única leitura do ambiente por processo | `docs/decisoes.md` | 1 |
| DT-03 | Dublês de sessão nos testes: `SessionSpy` (registra `close()`) para `get_db` e `FailingSession` (levanta `OperationalError` em `execute`) para `ping` e para o `503` de `/health`; substituição por `monkeypatch` e `dependency_overrides`, sem biblioteca de *mock* | `docs/decisoes.md` | 2 |

Motivo da DT-01: sem a fábrica, a aplicação usaria o *engine* de `DATABASE_URL` no `lifespan` e criaria `tasks.db` na raiz durante os testes (RT-04, critério 4), e não haveria como testar `ENVIRONMENT=production` sem recarregar módulos (RF-13). Alternativa descartada: `importlib.reload` de `app.main` com variáveis de ambiente alteradas (frágil e dependente da ordem dos testes).

Arquivo novo em relação à [Estrutura de diretórios](../CLAUDE.md#estrutura-de-diretórios) do `CLAUDE.md`: `app/models/health_schemas.py` (D-08), dentro de um pacote existente, como a estrutura permite. Nenhum diretório novo.

## 3. Verificação prévia

Os trechos de código deste *blueprint* foram executados em protótipo fora do repositório (diretório temporário do assistente), em 05/10/2026, no `.venv` do projeto (Python 3.14.6 e as versões do `requirements.txt`): 13 testes passando com `python -m pytest -W error`, `python -m mypy --explicit-package-bases app` sem erros, `python -m uvicorn app.main:app` respondendo `200` em `/health` e `/docs`, e nenhum arquivo criado pelos testes.

## 4. APIs: permitidas e proibidas

### 4.1 Importações permitidas

Usar exatamente estas linhas, por arquivo. Nenhuma outra importação de terceiros.

```python
# app/models/settings.py
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# app/models/base.py
from sqlalchemy.orm import DeclarativeBase

# app/models/health_schemas.py
from typing import Literal
from pydantic import BaseModel

# app/repositories/database.py
import logging
from collections.abc import Iterator
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from app.models.base import Base
from app.models.settings import get_settings

# app/services/health_service.py
from sqlalchemy.orm import Session
from app.models.health_schemas import HealthRead
from app.repositories.database import ping

# app/api/health_routes.py
from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.models.health_schemas import HealthRead
from app.repositories.database import get_db
from app.services.health_service import check_health

# app/main.py
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Engine
from app.api.health_routes import router as health_router
from app.models.settings import Settings, get_settings
from app.repositories.database import create_tables, engine

# tests/test_task_routes.py
import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
import app.main as main_module
from app.main import create_app
from app.models.settings import Environment, Settings
from app.repositories import database
from app.repositories.database import get_db, ping
```

### 4.2 Padrões proibidos

Do roteiro de checagem do `CLAUDE.md` (verificado em 03 e 04/10/2026 nas versões fixadas):

| Proibido | Usar |
| --- | --- |
| `@app.on_event("startup")`, `on_startup=` | `FastAPI(lifespan=...)` com `@asynccontextmanager` |
| `class Config:` em `BaseModel` ou `BaseSettings` | `model_config = SettingsConfigDict(...)` (e `ConfigDict` em modelos, a partir da `v0.3.0`) |
| `datetime.utcnow()` | `datetime.now(UTC)` (não há datas nesta *release*) |
| `declarative_base()` | `class Base(DeclarativeBase)` |
| `httpx` | `httpx2` (já fixado no `requirements.txt`; o `TestClient` o usa sem importação explícita) |
| *engine* de teste sem `engine.dispose()` | `engine.dispose()` no encerramento da *fixture* |
| `mypy app` | `python -m mypy --explicit-package-bases app` |

Também proibidos nesta *release*: SQL por concatenação ou *f-string* (só `text("SELECT 1")`, literal fixo); `type X = ...` (sintaxe do Python 3.12; o mínimo do projeto é 3.11, usar atribuição simples `X = Literal[...]`); `Any` e `# type: ignore` no código de `app/`; `__init__.py` em `app/` (ADR-03).

## 5. Passos

Cada passo termina com a definição de pronto verde:

```bash
python -m pytest -W error
python -m mypy --explicit-package-bases app
```

### Passo 1: configuração (RT-01, RT-04)

**Arquivos a criar:**

- Os `__init__.py` dos quatro pacotes, cada um com uma única linha, a *docstring* abaixo:
  - `app/models/__init__.py`: `"""Estruturas de dados: modelos ORM, esquemas Pydantic e configurações, sem lógica."""`
  - `app/repositories/__init__.py`: `"""Acesso ao banco: engine, sessão e consultas, sem regra de negócio."""`
  - `app/services/__init__.py`: `"""Regras de negócio, sem conhecimento de HTTP."""`
  - `app/api/__init__.py`: `"""Rotas HTTP, sem acesso ao banco nem regra de negócio."""`
- `app/models/settings.py`.
- `tests/test_task_routes.py` (só os testes deste passo).
- `docs/decisoes.md`, com o cabeçalho do arquivo e a DT-02 (formato da seção "Decisões técnicas" do `CLAUDE.md`: data e *release*; contexto; decisão; alternativas descartadas; consequências; IDs relacionados).

**`app/models/settings.py`:**

- `Environment = Literal["development", "test", "production"]`: tipo dos ambientes aceitos.
- `class Settings(BaseSettings)`: campos `database_url: str = "sqlite:///./tasks.db"` e `environment: Environment = "development"`. Os nomes das variáveis de ambiente são `DATABASE_URL` e `ENVIRONMENT` (o pydantic-settings não diferencia maiúsculas). Valor de `ENVIRONMENT` fora do conjunto levanta `pydantic.ValidationError` na construção. Os padrões são os do README (Configuração) e este é o único arquivo com literais de configuração.
- `def get_settings() -> Settings`, decorada com `@lru_cache(maxsize=1)`: devolve a instância única de `Settings` lida do ambiente e do `.env` (DT-02).

Trecho sensível:

```python
Environment = Literal["development", "test", "production"]


class Settings(BaseSettings):
    """<docstring em português>"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///./tasks.db"
    environment: Environment = "development"
```

**Testes** (`tests/test_task_routes.py`). Todos constroem `Settings(_env_file=None)` ou apontam `_env_file` para `tmp_path`, para não depender de um `.env` local:

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_settings_use_readme_defaults_without_environment` | `monkeypatch.delenv` de `DATABASE_URL` e `ENVIRONMENT` (`raising=False`); `Settings(_env_file=None)` | `database_url == "sqlite:///./tasks.db"` e `environment == "development"` |
| `test_settings_read_values_from_environment_variables` | `monkeypatch.setenv("DATABASE_URL", "sqlite:///./outro.db")` e `setenv("ENVIRONMENT", "production")`; `Settings(_env_file=None)` | valores iguais aos definidos |
| `test_settings_read_values_from_env_file` | variáveis removidas; arquivo `tmp_path / ".env"` com `DATABASE_URL=sqlite:///./arquivo.db` e `ENVIRONMENT=test` (UTF-8); `Settings(_env_file=env_file)` | `database_url == "sqlite:///./arquivo.db"` e `environment == "test"` |
| `test_settings_reject_environment_outside_allowed_values` | `monkeypatch.setenv("ENVIRONMENT", "staging")`; `Settings(_env_file=None)` | levanta `ValidationError` |

**Verificação:** definição de pronto; 4 testes passando; mypy sem erros.

**IDs:** RT-01 (critérios 1 a 4), RT-04, RNF-07, DT-02.

### Passo 2: base declarativa e acesso ao banco (RT-02, RT-04)

**Arquivos a criar:** `app/models/base.py`, `app/repositories/database.py`. **A alterar:** `tests/test_task_routes.py`, `docs/decisoes.md` (DT-03).

**`app/models/base.py`:** `class Base(DeclarativeBase)`, só com *docstring* (ADR-02). Nenhum modelo nesta *release*; `Task` chega na `v0.3.0`.

**`app/repositories/database.py`:**

- `logger = logging.getLogger(__name__)`.
- `def create_db_engine(database_url: str) -> Engine`: devolve `create_engine(database_url, connect_args={"check_same_thread": False})` (ADR-04). Não conecta.
- `engine: Engine = create_db_engine(get_settings().database_url)`, no nível do módulo. O *engine* é preguiçoso: importar o módulo não cria o arquivo do banco.
- `SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)`.
- `def get_db() -> Iterator[Session]`: cria `session = SessionLocal()`, entrega com `yield` dentro de `try` e chama `session.close()` no `finally`, inclusive quando a requisição levanta exceção. Não faz `commit` (ADR-12). Usa o nome global `SessionLocal` a cada chamada (os testes o substituem por `monkeypatch`); não usar `with SessionLocal() as session`.
- `def create_tables(db_engine: Engine) -> None`: executa `Base.metadata.create_all(bind=db_engine)` (ADR-05). Chamada só pelo `lifespan` de `app/main.py`.
- `def ping(session: Session) -> bool`: executa `session.execute(text("SELECT 1"))` e devolve `True`; em `SQLAlchemyError`, chama `logger.exception("Falha ao verificar a conexão com o banco de dados")` e devolve `False`. Não propaga a exceção (ADR-07).

**Testes** (`tests/test_task_routes.py`). Acrescentar os dublês e a *fixture* de *engine*:

```python
class FailingSession:
    """Dublê de sessão cujo execute falha como um banco indisponível (DT-03)."""

    def execute(self, *args: object, **kwargs: object) -> None:
        """Levanta OperationalError com SQL e detalhe que não podem vazar na resposta."""
        raise OperationalError("SELECT 1", {}, Exception("database is locked"))

    def close(self) -> None:
        """Não há recurso a liberar."""


class SessionSpy:
    """Dublê de sessão que registra o fechamento (DT-03)."""

    def __init__(self) -> None:
        self.is_closed = False

    def close(self) -> None:
        """Marca a sessão como fechada."""
        self.is_closed = True


@pytest.fixture
def test_engine() -> Iterator[Engine]:
    """Engine SQLite em memória compartilhado entre conexões (ADR-06)."""
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    yield engine
    engine.dispose()
```

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_get_db_closes_session_after_request` | `monkeypatch.setattr(database, "SessionLocal", lambda: spy)`; `generator = get_db()`; `next(generator)`; segundo `next` | primeiro `next` devolve `spy`; segundo levanta `StopIteration`; `spy.is_closed` |
| `test_get_db_closes_session_when_request_fails` | mesma substituição; `next(generator)`; `generator.throw(RuntimeError("falha simulada"))` | levanta `RuntimeError`; `spy.is_closed` |
| `test_ping_returns_true_when_database_is_available` | `with Session(test_engine) as session: ping(session)` | `True` |
| `test_ping_returns_false_and_logs_when_database_fails` | `with caplog.at_level(logging.ERROR, logger="app.repositories.database"): ping(FailingSession())` | `False`; `"database is locked" in caplog.text` |

**Verificação:** definição de pronto; 8 testes passando; nenhum arquivo `tasks.db` criado na raiz.

**IDs:** RT-02 (critérios 1 a 4), RT-04 (critérios 1 e 2, *fixture* de *engine*), ADR-02, ADR-04, ADR-06, ADR-07, ADR-12, RNF-09, RNF-12, DT-03.

### Passo 3: esquema e *service* de saúde (RF-12, D-08)

**Arquivos a criar:** `app/models/health_schemas.py`, `app/services/health_service.py`. **A alterar:** `docs/arquitetura.md` (ADR-13 na tabela da seção 6, com o contrato da D-08), `docs/escopo-mvp.md` (D-08 marcada como decidida, com referência ao ADR-13 e a este *blueprint*).

**`app/models/health_schemas.py`:**

- `HealthStatus = Literal["ok", "unavailable"]`.
- `class HealthRead(BaseModel)`: campos `status: HealthStatus` (aplicação) e `database: HealthStatus` (banco). Sem lógica.

**`app/services/health_service.py`:**

- `def check_health(session: Session) -> HealthRead`: chama `ping(session)`; se `True`, devolve `HealthRead(status="ok", database="ok")`; se `False`, `HealthRead(status="unavailable", database="unavailable")`. Não conhece HTTP nem códigos de *status*. O nome `check_health` substitui o `check` do diagrama de `/health` (ajuste no fechamento).

**Testes:** sem teste novo neste passo; o *service* é coberto pelos testes de rota do passo 4 (o `tests/test_task_service.py` é reservado ao *service* de tarefas).

**Verificação:** definição de pronto; 8 testes passando; mypy sem erros nos dois arquivos novos.

**IDs:** RF-12 (critérios 3 e 4), D-08, ADR-07, ADR-13.

### Passo 4: rota, composição e testes de integração (RT-03, RT-04, RF-12, RF-13)

**Arquivos a criar:** `app/api/health_routes.py`, `app/main.py`. **A alterar:** `tests/test_task_routes.py`, `docs/decisoes.md` (DT-01).

**`app/api/health_routes.py`:**

- `router = APIRouter(tags=["health"])`.
- `def read_health(response: Response, session: Annotated[Session, Depends(get_db)]) -> HealthRead`, registrada com `@router.get("/health", response_model=HealthRead, responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthRead}})`. Chama `check_health(session)`; se `health.status == "unavailable"`, define `response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE`; devolve o `HealthRead`. Não executa SQL nem toca a sessão além de repassá-la.

**`app/main.py`:** só composição (RT-03, critério 3).

- `def create_app(settings: Settings, db_engine: Engine) -> FastAPI`: define o `lifespan`, cria a aplicação com a documentação desabilitada quando `settings.environment == "production"` (ADR-08), registra `health_router` e devolve a aplicação (DT-01).
- `app = create_app(get_settings(), engine)`, no nível do módulo, para `python -m uvicorn app.main:app`.
- O `lifespan` chama `create_tables` pelo nome importado no módulo (o teste o substitui em `app.main`).

Trecho sensível:

```python
def create_app(settings: Settings, db_engine: Engine) -> FastAPI:
    """<docstring em português>"""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        create_tables(db_engine)
        yield

    is_production = settings.environment == "production"
    application = FastAPI(
        title="To-Do List API",
        lifespan=lifespan,
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )
    application.include_router(health_router)
    return application


app = create_app(get_settings(), engine)
```

**Testes** (`tests/test_task_routes.py`). Acrescentar os auxiliares e as *fixtures* de cliente:

```python
def build_get_db_override(
    session_factory: sessionmaker[Session],
) -> Callable[[], Iterator[Session]]:
    """Devolve um substituto de get_db ligado ao engine de teste."""

    def override_get_db() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    return override_get_db


@contextmanager
def open_test_client(environment: Environment, engine: Engine) -> Iterator[TestClient]:
    """Abre um TestClient com o ambiente pedido e get_db apontando para o engine de teste."""
    application = create_app(Settings(_env_file=None, environment=environment), engine)
    application.dependency_overrides[get_db] = build_get_db_override(sessionmaker(bind=engine))
    try:
        with TestClient(application) as client:
            yield client
    finally:
        application.dependency_overrides.clear()


@pytest.fixture
def client(test_engine: Engine) -> Iterator[TestClient]:
    """Cliente de integração com ENVIRONMENT=test e banco em memória."""
    with open_test_client("test", test_engine) as test_client:
        yield test_client


@pytest.fixture
def failing_db_client(test_engine: Engine) -> Iterator[TestClient]:
    """Cliente cuja sessão de banco falha em toda consulta."""
    application = create_app(Settings(_env_file=None, environment="test"), test_engine)

    def override_get_db() -> Iterator[FailingSession]:
        yield FailingSession()

    application.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(application) as test_client:
            yield test_client
    finally:
        application.dependency_overrides.clear()
```

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_lifespan_creates_tables_on_startup` | `created_on: list[Engine] = []`; `monkeypatch.setattr(main_module, "create_tables", created_on.append)`; `create_app(Settings(_env_file=None, environment="test"), test_engine)`; `with TestClient(application): pass` | `created_on == [test_engine]` |
| `test_health_returns_200_when_database_is_available` | *fixture* `client`; `GET /health` | `200`; `json() == {"status": "ok", "database": "ok"}` |
| `test_health_returns_503_without_internal_details_when_database_fails` | *fixture* `failing_db_client`; `GET /health` | `503`; `json() == {"status": "unavailable", "database": "unavailable"}`; o texto da resposta não contém `"SELECT"`, `"Traceback"` nem `"locked"` |
| `test_docs_available_in_development` | `with open_test_client("development", test_engine)`; `GET /docs` e `GET /openapi.json` | ambos `200` |
| `test_docs_disabled_in_production` | `with open_test_client("production", test_engine)`; `GET /docs`, `/redoc` e `/openapi.json` | todos `404` |

**Verificação:** definição de pronto; 13 testes passando; `git status` sem arquivos novos além dos deste *blueprint* (nenhum `tasks.db`).

**IDs:** RT-03 (critérios 1 a 3), RT-04 (critérios 1 a 4), RF-12 (critérios 1 e 2), RF-13 (critérios 1 e 2), ADR-05, ADR-06, ADR-08, ADR-09, RNF-10, DT-01.

### Passo 5: execução manual (RT-03, critério 4)

**Comandos**, da raiz, com o `.venv` ativo (PowerShell):

```powershell
python -m uvicorn app.main:app --reload
# em outro terminal:
Invoke-RestMethod http://127.0.0.1:8000/health
```

**Resultado esperado:** o log do *uvicorn* mostra `Application startup complete.`; a resposta é `status: ok` e `database: ok`; `http://127.0.0.1:8000/docs` abre no navegador. O arquivo `tasks.db` criado na raiz é ignorado pelo `.gitignore` (`*.db`) e não aparece no `git status`. Encerrar o servidor com Ctrl+C.

**IDs:** RT-03 (critério 4), RF-12.

### Passo 6: fechamento (Prompt 24)

Arquivos dependentes a atualizar, conforme "Fechamento de release" e "Arquivos a manter atualizados" do `CLAUDE.md`:

| Arquivo | Atualização |
| --- | --- |
| `README.md` | status; Roadmap com a `v0.2.0` concluída; seção Endpoints com `GET /health` (200 e 503, com os corpos da D-08); Como rodar sem a nota "passam a valer a partir da `v0.2.0`"; Uso de IA generativa (modelo de execução dos Prompts 22 e 23) |
| `docs/arquitetura.md` | diagrama de módulos: nó `health_schemas.py` com as setas de `health_routes` e `health_service`, `main.py` → `create_tables`; diagrama de `/health`: `check(session)` → `check_health(session)`; observação sobre `create_app` (DT-01) |
| `docs/mermaid.md` | nova seção com o antes e o depois dos dois diagramas alterados |
| `CLAUDE.md` | Estrutura de diretórios com `app/models/health_schemas.py` e `docs/decisoes.md` já criado; remoção da seção "Ponto de partida" |
| `docs/backlog.md` | RT-01 a RT-04, RF-12 e RF-13 como `concluído`, com as horas reais |
| `CHANGELOG.md` | seção `0.2.0`, agrupada por tipo de *commit* |
| `docs/HISTORY-IA.md` | entradas dos Prompts 21 a 24 e consolidação da *release* |
| `prompts/Prompt 22 ...`, `Prompt 23 ...`, `Prompt 24 ...` | registro da execução ao final de cada arquivo |

Depois da aprovação do fechamento: *commits* em *Conventional Commits* na *branch* `feat/base-tecnica`, *merge* `--no-ff` em `main`, *tag* anotada `v0.2.0`, *push* e definição de pronto em clone limpo.

## 6. Riscos

| Risco | Tratamento |
| --- | --- |
| Testes criarem `tasks.db` na raiz pelo `lifespan` | DT-01: os testes passam o *engine* em memória a `create_app`; o *engine* do módulo é preguiçoso e nunca conecta nos testes |
| `ResourceWarning` de conexão aberta com `-W error` | `engine.dispose()` na *fixture* `test_engine`; sessões fechadas no `finally` de `get_db` e do substituto |
| `.env` local do desenvolvedor alterar o resultado dos testes | `Settings(_env_file=None)` em todos os testes, ou `.env` em `tmp_path` |
| Vazamento de SQL ou de detalhe interno no `503` | `ping` captura `SQLAlchemyError` e só registra no log; teste confere a ausência de `SELECT`, `Traceback` e `locked` |
| Documentação exposta em produção | `docs_url`, `redoc_url` e `openapi_url` como `None` com `ENVIRONMENT=production`; teste com os três caminhos (ADR-08) |
| *Health check* que só reflete o processo | `ping` executa `SELECT 1` real; teste do `503` usa a sessão que falha (ADR-07, RNF-12) |
| Literal de configuração fora de `settings.py` | padrões só em `Settings`; `main.py` e `database.py` leem de `get_settings()` (RNF-07). A comparação com `"production"` é um valor do `Literal`, não configuração |
| Smart App Control bloquear o SQLAlchemy compilado | procedimento do README (Solução de problemas); o `.venv` atual já usa a versão em Python puro |

## 7. O que não fazer

- Não criar `conftest.py`, `pyproject.toml`, `pytest.ini`, `mypy.ini`, `setup.cfg`, `Makefile` nem `.env` versionado.
- Não criar `app/__init__.py` (ADR-03) nem diretórios novos.
- Não criar `app/models/task.py`, `task_schemas.py`, `task_repository.py`, `task_service.py`, `priority_advisor.py`, `task_routes.py`, `tests/test_task_service.py` nem `tests/test_priority_advisor.py`: são das `v0.3.0` e `v0.4.0`.
- Não adicionar nem mudar dependências no `requirements.txt`; não importar `httpx`.
- Não adicionar `logging.basicConfig` nem configuração de log: o *uvicorn* configura o log em execução, e o `caplog` captura nos testes.
- Não incluir no corpo do `503` mensagem de erro, nome de exceção ou SQL.
- Não alterar `docs/requerimentos.md`, `docs/PRE-HISTORY-IA.md`, `docs/EXTRA-HISTORY-IA.md`, `docs/release-review-010.md`, `docs/release-prompts-solon-020.md`, `LICENSE` nem `.gitignore`.
- Não comitar sem pedido.

## 8. Condição de parada

Se um passo falhar de forma não prevista (teste, mypy, aviso com `-W error`, importação), ou exigir decisão que este *blueprint* não traz, quem executa para, reporta a saída e não improvisa.

## 9. Estimativa

| Passo | Itens | Horas |
| --- | --- | --- |
| 1 | RT-01 | 0,5 |
| 2 | RT-02 | 1 |
| 3 | RF-12 (esquema e *service*), D-08 | 0,5 |
| 4 | RT-03, RT-04, RF-12 (rota), RF-13 | 1,75 |
| 5 | RT-03 (execução manual) | 0,25 |
| **Itens do backlog** | | **4** |
| *Blueprint* (este arquivo) e fechamento (passo 6) | fora das estimativas dos itens | 1,5 |
| **Total da *release*** | | **5,5** |

Os 4 h do backlog cobrem os itens; *blueprint* e fechamento não estão nas estimativas por item e consomem a folga do orçamento (18,5 h estimadas contra cerca de 30 h). As horas reais são registradas no backlog no fechamento.
