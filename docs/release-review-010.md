# Revisão de publicação: release v0.1.0

Checklist de publicação da *release* `v0.1.0` (fundação), com as alterações aprovadas, os testes realizados, os bloqueadores e as recomendações.

| Item | Valor |
| --- | --- |
| Data | 04/10/2026 |
| Revisor | Claude Opus 5.5, via Claude Code, com aprovação do autor |
| *Prompt* | [`prompts/Prompt 08 - revisao critica release 010`](../prompts/Prompt%2008%20-%20revisao%20critica%20release%20010) |
| Base revisada | `main` em `ba74cf4`, sincronizada com `origin/main` |
| *Branch* das correções | `docs/release-0.1.0` |
| Resultado | publicada, com *tag* anotada `v0.1.0` |

**Legenda de severidade:**

- **[B]:** bloqueava a publicação da `v0.1.0`.
- **[B-0.2]:** não bloqueava a `v0.1.0`, mas impedia o início do código na `v0.2.0`.
- **[R]:** recomendação.

## 1. Resumo

| # | Item | Severidade | Situação |
| --- | --- | --- | --- |
| 1.1 | Criar `CHANGELOG.md` com a seção `[0.1.0]` | B | aplicado |
| 1.2 | Não reescrever o histórico publicado; regra de *merge* no `CLAUDE.md` | R | aplicado |
| 1.3 | Descrição correta do `94f30f2` no CHANGELOG | R | aplicado |
| 2.1 | Registrar a checagem de APIs deprecadas no `CLAUDE.md` | B | aplicado |
| 2.2 | `mypy --explicit-package-bases` e ADR-11 | B-0.2 | aplicado |
| 3.1 | SQLAlchemy bloqueado pelo Smart App Control | B-0.2 | corrigido no `.venv` e documentado |
| 3.3 | Python 3.11 declarado, mas não testado | R | pendente para a `v1.0.0` |
| 4.1 | Cobertura do `.gitignore` | — | conforme |
| 4.2 | Seção Node.js do `.gitignore` | R | mantida |
| 5.1 | Fechamento do README | B | aplicado |
| 5.2 | Registro no Prompt 08 e no `HISTORY-IA.md` | B | aplicado |
| 5.3 | Migração do Ponto de partida do `CLAUDE.md` | B | aplicado |
| 5.4 | *Tag* `v0.1.0` e *push* | B | aplicado; Release no GitHub pendente |
| 5.5 | Testes e exemplos de uso | B para a `v1.0.0` | fora do escopo da `v0.1.0` |
| 5.6 | Nomes dos arquivos de *prompt* | R | regra ajustada, sem renomear |
| 5.7 | Este arquivo na estrutura do `CLAUDE.md` | — | aplicado |

## 2. Commits e CHANGELOG

### Achados

- 8 *commits* sem *merge*, todos no padrão *Conventional Commits*, em português, com corpo listando as mudanças: `chore` ×2, `docs` ×5, `build` ×1. Isso atende ao requisito de "5 a 10 *commits* significativos" de [`requerimentos.md`](requerimentos.md).
- 3 *commits* de *merge* (`5a4eac1`, `dd4db2a`, `ba74cf4`) com a mensagem padrão do git. As ferramentas de *Conventional Commits* (por exemplo, o commitlint) ignoram esse formato por padrão.
- A mensagem do `94f30f2` ("inicializa repositório com estrutura do projeto") é imprecisa: o git não versiona diretórios vazios, então o *commit* contém só `.gitignore`, `CLAUDE.md` e o primeiro *prompt*.
- Nenhum *commit* direto em `main` além do inicial, que é inevitável.

### Alterações

- **1.1:** criado o [`CHANGELOG.md`](../CHANGELOG.md):
  - formato Keep a Changelog 1.1.0, com Versionamento Semântico;
  - seção `[0.1.0] - 2026-10-04`, agrupada por tipo de *commit* (`docs`, `build`, `chore`) e com os *hashes*;
  - o arquivo foi incluído na estrutura fechada, nas fontes de verdade, na tabela de arquivos a manter e no fechamento de *release* do `CLAUDE.md`.
- **1.2:** o histórico não foi reescrito, porque já estava publicado e exigiria *force push*. O `CLAUDE.md` (seção Git) passou a registrar duas regras:
  - *merge* com `--no-ff` e mensagem padrão do git;
  - *tag* anotada `vX.Y.Z` por *release*.
- **1.3:** o CHANGELOG descreve o `94f30f2` pelo que ele de fato contém.

## 3. APIs deprecadas

Não há código em `app/` nesta *release*, então nenhuma substituição em código foi necessária. Endpoints e banco não foram alterados.

### Método

Segui o roteiro do `CLAUDE.md`. Para cada padrão suspeito, escrevi um teste mínimo do padrão legado e outro do substituto, e rodei os dois com `python -m pytest -W error -p no:cacheprovider` no `.venv` do projeto, já corrigido (item 3.1).

- Os testes ficaram fora do repositório, porque a estrutura de `tests/` é fechada em três arquivos; o código está no [Apêndice A](#apêndice-a-testes-mínimos-da-checagem).
- Para o padrão do mypy, simulei a estrutura da ADR-03 num diretório temporário: `app/` sem `__init__.py`, subpacotes com `__init__.py` e importações absolutas `app.*`.

### Resultado

`5 failed, 11 passed in 0.43s`. As falhas são esperadas: correspondem aos padrões legados.

| Padrão | Teste | Resultado | Situação |
| --- | --- | --- | --- |
| `@app.on_event("startup")` | legado | falha: `DeprecationWarning` | proibido |
| `FastAPI(lifespan=...)` | substituto | passa | permitido |
| `class Config` em `BaseModel` | legado | falha: `PydanticDeprecatedSince20` | proibido |
| `model_config = ConfigDict(...)` | substituto | passa | permitido |
| `class Config` em `BaseSettings` | legado | falha: `PydanticDeprecatedSince20` | proibido |
| `SettingsConfigDict(env_file=".env")` | substituto | passa | permitido |
| `datetime.utcnow()` | legado | falha: `DeprecationWarning` | proibido |
| `datetime.now(datetime.UTC)` | substituto | passa | permitido |
| `declarative_base()` | legado | passa, sem aviso | estilo legado, evitar |
| `class Base(DeclarativeBase)` com `Mapped` | substituto | passa | permitido |
| `TestClient` com `httpx2` | substituto | passa | permitido |
| fixture `sqlite://` + `StaticPool` sem `dispose()` | legado | falha no `gc` seguinte: `ResourceWarning: unclosed database`, convertido em `PytestUnraisableExceptionWarning` | proibido |
| fixture com `engine.dispose()` | substituto | passa | permitido |
| `python -m mypy app` | legado | código 2: `Source file found twice under different module names: "models.x" and "app.models.x"` | proibido |
| `python -m mypy --explicit-package-bases app` | substituto | `Success: no issues found in 5 source files` | permitido |

Versões testadas: FastAPI 0.142.2, Starlette 1.7.0, Pydantic 2.13.5, pydantic-settings 2.15.0, SQLAlchemy 2.1.3, pytest 9.1.1, mypy 2.4.0 e Python 3.14.6.

### Alterações

- **2.1:** a tabela do roteiro de checagem no `CLAUDE.md` foi preenchida com a situação, a versão e a data de cada padrão.
- **2.2:** o comando da definição de pronto passou a ser `python -m mypy --explicit-package-bases app` no `CLAUDE.md` e no README, e a ADR-11 foi registrada em [`arquitetura.md`](arquitetura.md).
  - Alternativa descartada: criar `app/__init__.py`, que contraria a ADR-03 e a estrutura fechada.

## 4. Ambiente virtual

### Achados

- `.venv` criado com Python 3.14.6 (`include-system-site-packages = false`) e pip 26.2.1.
- `pip check`: "No broken requirements found".
- `pip freeze` é idêntico ao `requirements.txt`: 31 pacotes e versões, desconsiderando os marcadores de plataforma.
- `.venv/` é ignorado pelo git (`git status --ignored`).
- **3.1 [B-0.2]:** `import sqlalchemy` falhava com `ImportError: DLL load failed while importing _immutabledict_cy: Uma política de Controle de Aplicativo bloqueou este arquivo`.
  - Causa: o Smart App Control do Windows está ativo (`VerifiedAndReputablePolicyState = 1`) e bloqueia as 8 extensões `.pyd` do SQLAlchemy, que não são assinadas.
  - As extensões compiladas de `pydantic_core`, `mypy`, `librt` e `ast_serialize` carregam normalmente.
  - O erro se reproduz num ambiente virtual limpo, criado a partir do `requirements.txt`, então não é defeito do `.venv` local.

### Correção aplicada (3.1)

Testei a correção primeiro num ambiente virtual temporário e depois a apliquei ao `.venv`:

```powershell
$env:DISABLE_SQLALCHEMY_CEXT="1"
python -m pip install --force-reinstall --no-deps --no-binary SQLAlchemy SQLAlchemy==2.1.3
```

Resultado:

- `sqlalchemy.__version__ == "2.1.3"`;
- nenhum `.pyd` restante no pacote;
- `pip check` sem conflitos.

A versão, a API e o comportamento são os mesmos; só as otimizações em Cython ficam de fora. O `requirements.txt` não mudou. O procedimento está documentado no README, em Solução de problemas (Windows), porque um avaliador com o Smart App Control ativo encontraria o mesmo erro.

### Recomendação (3.3)

O README declara o Python 3.11 como mínimo (exigência do SQLAlchemy 2.1), mas só o 3.14.6 está instalado e foi testado. Proponho validar em 3.11 na `v1.0.0`, ou declarar apenas a versão testada.

## 5. Cobertura do `.gitignore`

Verificado com `git check-ignore -v`:

| Caminho de exemplo | Resultado | Regra |
| --- | --- | --- |
| `tasks.db`, `tasks.db-journal`, `tasks.db-wal` | ignorado | `*.db`, `*.db-journal`, `*.db-wal` |
| `.env`, `.env.production` | ignorado | `.env`, `.env.*` |
| `.env.example` | versionável | `!.env.example` |
| `app/__pycache__/x.pyc` | ignorado | `__pycache__/` |
| `.pytest_cache/`, `.mypy_cache/` | ignorado | regras próprias |
| `.vscode/settings.json` | ignorado | `.vscode/` |
| `.venv/` | ignorado | `.venv/` |
| `app/main.py`, `tests/test_x.py`, `CHANGELOG.md`, `docs/release-review-010.md` | versionável | — |

- **4.1:** a cobertura está conforme a *stack* (Python, `.venv`, pytest, mypy, `.env`, SQLite, VS Code, sistemas operacionais).
- **4.2 [R]:** a seção Node.js antecipa um *frontend* que está fora do MVP, o que contraria a regra de não antecipar configuração. Foi mantida porque foi pedido explícito do Prompt 01 e não tem efeito colateral.

## 6. Requisitos do curso e outros itens da release

Conferência contra [`requerimentos.md`](requerimentos.md):

| Requisito | Situação na `v0.1.0` |
| --- | --- |
| Repositório público, sem informações sensíveis | conforme: a API do GitHub retorna `"visibility": "public"`, e a busca por chaves, senhas e *tokens* no histórico (`git log -p --all`) não encontrou nada |
| Histórico de *commits* consistente (5 a 10, *Conventional Commits*) | conforme (seção 2) |
| README: título, descrição, como rodar, tecnologias com modelos de IA, limitações e próximos passos, créditos e licença | conforme |
| README: exemplos de uso da API | pendente: não há endpoints até a `v0.3.0` |
| Gerenciamento de dependências | conforme: `requirements.txt` fixado e verificado |
| Testes automatizados executáveis e passando | pendente: não há código; previstos a partir da `v0.2.0` |
| *Release* ou *tag* | *tag* `v0.1.0` criada; *tag* e Release `v1.0.0` previstas para a entrega |

### Alterações

- **5.1:** README:
  - status atualizado;
  - roadmap com a `v0.1.0` concluída;
  - tabela de uso de IA completa (inclui o Claude in Chrome);
  - link para o CHANGELOG;
  - comando do mypy (2.2) e Solução de problemas (3.1).
- **5.2:** registros no Prompt 08 e no `HISTORY-IA.md`.
- **5.3:** o Ponto de partida do `CLAUDE.md` foi reduzido às decisões em aberto (regras da prioridade 4, prioridade padrão, filtro por prioridade e função do `priority_advisor`). O restante já está no README. A seção Inicialização do projeto foi marcada como concluída.
- **5.4:** *merge* de `docs/release-0.1.0` em `main`, *tag* anotada `v0.1.0` e *push* de `main` e da *tag*.
  - A Release no GitHub não foi criada, porque o `gh` não está instalado. Para criá-la manualmente, use a interface web, em *Releases* → *Draft a new release* → *tag* `v0.1.0`, com o texto da seção `[0.1.0]` do CHANGELOG.
- **5.6:** a regra de nomes do `CLAUDE.md` passou a ser `Prompt NN - <título>`, que é a prática dos *prompts* 01 a 08. O `Prompt00 - Inicio` mantém o nome original, para não quebrar os links do histórico.
- **5.7:** este arquivo foi incluído na estrutura de `docs/` do `CLAUDE.md`.

## 7. Testes realizados

| Teste | Comando | Resultado |
| --- | --- | --- |
| Definição de pronto: testes | `python -m pytest -W error` | `no tests ran` (código 5): não aplicável, porque não há testes na `v0.1.0` |
| Definição de pronto: tipos | `python -m mypy --explicit-package-bases app` | `There are no .py[i] files in directory 'app'` (código 2): não aplicável, porque não há código na `v0.1.0` |
| Checagem de APIs deprecadas | `python -m pytest -W error -p no:cacheprovider` (Apêndice A) | 11 passaram e 5 falharam como esperado (seção 3) |
| Estrutura de pacotes no mypy | `mypy app` e `mypy --explicit-package-bases app`, na estrutura simulada | código 2 e sucesso, respectivamente |
| Integridade do `.venv` | `pip check` e `pip freeze` contra o `requirements.txt` | sem conflitos; idêntico |
| Importação dos pacotes | `import` de cada pacote direto | todos importam, depois da correção 3.1 |
| Instalação limpa | `python -m venv` + `pip install -r requirements.txt` em diretório temporário | instala; falha no `import sqlalchemy` com o Smart App Control ativo; corrigido com 3.1 |
| `.gitignore` | `git check-ignore -v` | conforme (seção 5) |
| Visibilidade e segredos | API do GitHub e `git log -p --all` | público; nenhuma ocorrência |

A definição de pronto não se aplica a esta *release*, que não tem código, e foi registrada como "não aplicável", não como aprovada. Ela passa a valer na `v0.2.0`.

## 8. Bloqueadores e sugestões

### Bloqueadores da `v0.1.0`

Todos resolvidos: 1.1, 2.1, 5.1, 5.2, 5.3 e 5.4.

### Bloqueadores das próximas releases

- **v0.2.0:** 2.2 e 3.1 (resolvidos nesta revisão). O primeiro código deve seguir a tabela do roteiro de checagem: `lifespan`, `ConfigDict`/`SettingsConfigDict`, `now(UTC)`, `DeclarativeBase`, `engine.dispose()` e `httpx2`.
- **v1.0.0:**
  - testes automatizados passando com `-W error`;
  - exemplos de uso no README;
  - *tag* e Release `v1.0.0` no GitHub.

### Recomendações em aberto

- **3.3:** validar em Python 3.11, ou declarar só a versão testada.
- **5.4:** criar a Release `v0.1.0` na interface web do GitHub.
- Instalar o GitHub CLI (`gh`) para automatizar as Releases a partir da `v0.2.0`.

## Apêndice A: testes mínimos da checagem

Executados fora do repositório, no diretório temporário da sessão, com o `.venv` do projeto.

`test_dep.py`:

```python
"""Testes mínimos do roteiro de checagem de APIs deprecadas (fora do repositório)."""
import datetime as dt
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.pool import StaticPool


# ---------- padrões suspeitos (espera-se aviso/erro) ----------
def test_on_event_legacy() -> None:
    app = FastAPI()
    @app.on_event("startup")
    def _s() -> None: ...
    with TestClient(app):
        pass

def test_pydantic_class_config_legacy() -> None:
    class M(BaseModel):
        x: int
        class Config:
            frozen = True

def test_settings_class_config_legacy() -> None:
    class S(BaseSettings):
        a: str = "x"
        class Config:
            env_file = ".env"
    S()

def test_utcnow_legacy() -> None:
    dt.datetime.utcnow()

def test_declarative_base_legacy() -> None:
    from sqlalchemy.orm import declarative_base
    declarative_base()

def test_engine_without_dispose_legacy() -> None:
    eng = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    with eng.connect() as c:
        c.execute(text("SELECT 1"))
    del eng
    import gc; gc.collect()

# ---------- substitutos (espera-se passar limpo) ----------
def test_lifespan_ok() -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
    app = FastAPI(lifespan=lifespan)
    @app.get("/ping")
    def ping() -> dict[str, str]:
        return {"ok": "1"}
    with TestClient(app) as c:
        assert c.get("/ping").status_code == 200

def test_configdict_ok() -> None:
    class M(BaseModel):
        model_config = ConfigDict(frozen=True)
        x: int
    M(x=1)

def test_settingsconfigdict_ok() -> None:
    class S(BaseSettings):
        model_config = SettingsConfigDict(env_file=".env")
        a: str = "x"
    S()

def test_now_utc_ok() -> None:
    assert dt.datetime.now(dt.UTC).tzinfo is dt.UTC

def test_declarativebase_ok() -> None:
    class Base(DeclarativeBase): ...
    class T(Base):
        __tablename__ = "t"
        id: Mapped[int] = mapped_column(primary_key=True)
        title: Mapped[str] = mapped_column(String(100))
    eng = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(eng)
    with Session(eng) as s:
        s.add(T(title="a")); s.commit()
    eng.dispose()

def test_testclient_transport_ok() -> None:
    import httpx2  # noqa: F401
    app = FastAPI()
    with TestClient(app) as c:
        assert c.get("/nao-existe").status_code == 404
```

O `test_engine_without_dispose_legacy` passa isoladamente, porque o `del` seguido de `gc.collect()` dentro do próprio teste não chega a disparar o aviso. O vazamento foi demonstrado com uma *fixture* em `test_leak.py`:

```python
import gc
from collections.abc import Iterator
import pytest
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.pool import StaticPool

@pytest.fixture
def engine_sem_dispose() -> Iterator[Engine]:
    eng = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    yield eng

@pytest.fixture
def engine_com_dispose() -> Iterator[Engine]:
    eng = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    yield eng
    eng.dispose()

def test_a_sem_dispose(engine_sem_dispose: Engine) -> None:
    with engine_sem_dispose.connect() as c:
        c.execute(text("SELECT 1"))

def test_b_gc() -> None:          # falha: ResourceWarning da fixture sem dispose()
    gc.collect()

def test_c_com_dispose(engine_com_dispose: Engine) -> None:
    with engine_com_dispose.connect() as c:
        c.execute(text("SELECT 1"))

def test_d_gc() -> None:          # passa
    gc.collect()
```
