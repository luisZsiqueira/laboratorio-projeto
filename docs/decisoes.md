# Decisões técnicas

Registro das decisões técnicas de implementação (DT) que não estão no *blueprint* de uma *release* nem nos ADRs de [`docs/arquitetura.md`](arquitetura.md), e que outra pessoa precisaria conhecer para manter o código. Formato e limite com os ADRs: `CLAUDE.md`, seção "Decisões técnicas". Cada DT nasce no mesmo *commit* do código que a aplica.

## DT-02: `get_settings()` com `lru_cache(maxsize=1)`

- **Data e *release*:** 05/10/2026, `v0.2.0`.
- **Contexto:** a configuração vem só do ambiente e do `.env` (RNF-07). `database.py` e `main.py` precisam das mesmas `Settings`, e reler o ambiente e o arquivo `.env` a cada uso é desperdício e permite resultados diferentes dentro do mesmo processo.
- **Decisão:** `app/models/settings.py` expõe `get_settings()`, decorada com `functools.lru_cache(maxsize=1)`, que devolve uma única instância de `Settings` por processo. Os testes não usam `get_settings()`: constroem `Settings(_env_file=None)` (ou com `_env_file` em `tmp_path`) para não depender do ambiente nem de um `.env` local.
- **Alternativas descartadas:** variável global `settings = Settings()` no nível do módulo, porque lê o ambiente na importação e dificulta os testes; instanciar `Settings()` a cada uso, porque relê o ambiente e o `.env` repetidamente.
- **Consequências:** alterar variáveis de ambiente depois da primeira chamada não tem efeito no processo (para os testes, `get_settings.cache_clear()` ou `Settings` próprio). A configuração só muda reiniciando a aplicação.
- **IDs relacionados:** RT-01, RNF-07.

## DT-03: dublês de sessão nos testes, sem biblioteca de *mock*

- **Data e *release*:** 05/10/2026, `v0.2.0`.
- **Contexto:** `get_db` e `ping` precisam ser testados em dois cenários difíceis de provocar com um banco real: sessão que deve ser fechada ao fim da requisição (inclusive em erro) e banco indisponível.
- **Decisão:** duas classes simples em `tests/test_task_routes.py`. `SessionSpy` registra a chamada de `close()` e é usada nos testes de `get_db`, que substituem `database.SessionLocal` com `monkeypatch`. `FailingSession` levanta `OperationalError` em `execute` e é usada nos testes de `ping` e do `503` de `/health`, via `dependency_overrides`. Não se usa `unittest.mock` nem outra biblioteca de *mock*.
- **Alternativas descartadas:** `MagicMock`, porque aceita qualquer chamada e esconde erros de contrato; banco SQLite real indisponível (arquivo inexistente ou travado), porque depende do sistema de arquivos e do sistema operacional.
- **Consequências:** `get_db` usa o nome global `SessionLocal` a cada chamada, para que a substituição valha; os dublês só implementam os métodos que os testes exercitam e precisam acompanhar o contrato da `Session` se `ping` ou `get_db` passarem a usar outros métodos.
- **IDs relacionados:** RT-02, RT-04, ADR-06, ADR-07.

## DT-01: fábrica `create_app(settings, db_engine)` em `app/main.py`

- **Data e *release*:** 05/10/2026, `v0.2.0`.
- **Contexto:** a aplicação precisa criar as tabelas no `lifespan` (ADR-05) e desabilitar a documentação com `ENVIRONMENT=production` (ADR-08). Se `app/main.py` criasse a aplicação direto com o *engine* e as `Settings` do ambiente, os testes criariam `tasks.db` na raiz (RT-04, critério 4) e não haveria como testar `production` sem recarregar módulos (RF-13).
- **Decisão:** `app/main.py` expõe `create_app(settings: Settings, db_engine: Engine) -> FastAPI` e cria `app = create_app(get_settings(), engine)` no nível do módulo, para `python -m uvicorn app.main:app`. O `lifespan` chama `create_tables(db_engine)` pelo nome importado no módulo. Os testes criam a aplicação com `Settings(_env_file=None, environment=...)` e o *engine* em memória, e substituem `get_db` por `dependency_overrides`.
- **Alternativas descartadas:** `importlib.reload` de `app.main` com variáveis de ambiente alteradas, porque é frágil e depende da ordem dos testes.
- **Consequências:** `app/main.py` continua só com composição. Cada teste tem sua própria instância da aplicação, sem estado compartilhado. O *engine* do módulo `database.py` nunca conecta nos testes.
- **IDs relacionados:** RT-03, RT-04, RF-13, ADR-05, ADR-08.
