# Decisões técnicas

Registro das decisões técnicas de implementação (DT) que não estão no *blueprint* de uma *release* nem nos ADRs de [`docs/arquitetura.md`](arquitetura.md), e que outra pessoa precisaria conhecer para manter o código. Formato e limite com os ADRs: `CLAUDE.md`, seção "Decisões técnicas". Cada DT nasce no mesmo *commit* do código que a aplica.

## DT-01: fábrica `create_app(settings, db_engine)` em `app/main.py`

- **Data e *release*:** 05/10/2026, `v0.2.0`.
- **Contexto:** a aplicação precisa criar as tabelas no `lifespan` (ADR-05) e desabilitar a documentação com `ENVIRONMENT=production` (ADR-08). Se `app/main.py` criasse a aplicação direto com o *engine* e as `Settings` do ambiente, os testes criariam `tasks.db` na raiz (RT-04, critério 4) e não haveria como testar `production` sem recarregar módulos (RF-13).
- **Decisão:** `app/main.py` expõe `create_app(settings: Settings, db_engine: Engine) -> FastAPI` e cria `app = create_app(get_settings(), engine)` no nível do módulo, para `python -m uvicorn app.main:app`. O `lifespan` chama `create_tables(db_engine)` pelo nome importado no módulo. Os testes criam a aplicação com `Settings(_env_file=None, environment=...)` e o *engine* em memória, e substituem `get_db` por `dependency_overrides`.
- **Alternativas descartadas:** `importlib.reload` de `app.main` com variáveis de ambiente alteradas, porque é frágil e depende da ordem dos testes.
- **Consequências:** `app/main.py` continua só com composição. Cada teste tem sua própria instância da aplicação, sem estado compartilhado. O *engine* do módulo `database.py` nunca conecta nos testes.
- **IDs relacionados:** RT-03, RT-04, RF-13, ADR-05, ADR-08.

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

## DT-04: tipo de coluna `UTCDateTime` e função `utc_now()` em `app/models/base.py`

- **Data e *release*:** 05/10/2026, `v0.3.0`.
- **Contexto:** as datas devem ser *timezone-aware* em UTC na persistência e nos esquemas (ADR-10), mas o SQLite não guarda fuso horário: uma coluna `DateTime(timezone=True)` devolve valores sem `tzinfo`.
- **Decisão:** `app/models/base.py` expõe `utc_now()` (`datetime.now(UTC)`) e `UTCDateTime`, um `TypeDecorator[datetime]` sobre `DateTime`. Na escrita, converte para UTC e grava sem fuso; data/hora sem fuso levanta `ValueError` (o SQLAlchemy a reporta como `StatementError`). Na leitura, restaura `tzinfo=UTC`. As colunas de data do modelo `Task` usam `UTCDateTime` e `default=utc_now`.
- **Alternativas descartadas:** `DateTime(timezone=True)`, porque o SQLite não guarda fuso e a leitura volta sem `tzinfo`; conversão no *service*, porque deixaria a leitura direta do banco sem fuso e espalharia a regra fora dos modelos.
- **Consequências:** a conversão fica num único ponto e é coberta por testes de persistência. Valores gravados são sempre UTC; um fuso diferente só existe na entrada da API, onde `AwareDatetime` o exige e a conversão para UTC acontece na gravação.
- **IDs relacionados:** RT-05, ADR-10.

## DT-05: `TaskPatch` com campos opcionais e rejeição de `null` em campos obrigatórios

- **Data e *release*:** 05/10/2026, `v0.3.0`.
- **Contexto:** em `PATCH`, o cliente envia só os campos que quer alterar, e o *service* precisa distinguir "campo ausente" de "campo enviado com `null`". Gravar `null` em `title`, `status` ou `priority` violaria colunas obrigatórias e resultaria em erro `500`.
- **Decisão:** `TaskPatch` tem os cinco campos opcionais, com padrão `None`, e um `field_validator` (`reject_null`) que rejeita `null` explícito em `title`, `status` e `priority` com `422`. `description` e `due_at` aceitam `null` para limpar o valor. O *service* aplica só `model_dump(exclude_unset=True)`. `PATCH` com corpo `{}` responde `200` sem alterar nada.
- **Alternativas descartadas:** valor sentinela para "ausente", porque `exclude_unset` do Pydantic já distingue ausência de `null`; validar `null` no *service*, porque é validação de entrada, que pertence aos esquemas.
- **Consequências:** o validador não roda quando o campo está ausente (o padrão não é validado), o que mantém a ausência permitida. A regra vale para os três campos obrigatórios, e novos campos obrigatórios precisam entrar na lista do validador.
- **IDs relacionados:** RT-06, RF-06.

## DT-06: `created_at` e `updated_at` com o mesmo instante na criação

- **Data e *release*:** 05/10/2026, `v0.3.0`.
- **Contexto:** com `default=utc_now` nas duas colunas, cada uma chama o relógio por conta própria e os valores diferiram em 1 µs no protótipo, o que faz uma tarefa recém-criada parecer já alterada.
- **Decisão:** `TaskService.create_task` chama `utc_now()` uma vez e passa o resultado a `created_at` e `updated_at`. Nas alterações, `updated_at` muda pelo `onupdate=utc_now` da coluna. O `default=utc_now` das colunas fica como proteção para quem criar `Task` fora do *service*.
- **Alternativas descartadas:** dois `default` independentes, pela diferença de microssegundos; um `default` compartilhado por `Task.__init__`, porque os modelos não têm lógica.
- **Consequências:** na criação, `created_at == updated_at`, o que os testes verificam. A criação de `Task` fora do *service* pode voltar a produzir valores diferentes.
- **IDs relacionados:** RT-08, ADR-10.

## DT-07: dublê `InMemoryTaskRepository` em `tests/test_task_service.py`

- **Data e *release*:** 05/10/2026, `v0.3.0`.
- **Contexto:** os testes unitários do *service* devem rodar sem banco e sem biblioteca de *mock* (`CLAUDE.md`, Testes), e a idempotência de `complete_task` só se prova sabendo se houve gravação.
- **Decisão:** classe simples que satisfaz o `TaskStore`: dicionário `tasks` em memória, `id` sequencial atribuído em `add` e contador `save_count`, incrementado por `save`. Os testes de idempotência conferem `save_count == 1` depois de duas conclusões.
- **Alternativas descartadas:** `MagicMock` (já descartado na DT-03: aceita qualquer chamada e esconde erros de contrato); `TaskRepository` com SQLite em memória, porque isso testaria o *repository* de novo e não isolaria o *service*.
- **Consequências:** o dublê precisa acompanhar o `TaskStore` se o contrato mudar; o mypy não confere `tests/`, então a aderência ao `TaskStore` é verificada pelos testes. O `id` do dublê é `len(tasks) + 1` e pode repetir um número depois de uma exclusão; nenhum teste cria uma tarefa depois de excluir outra, e um teste que precise disso exige um contador próprio.
- **IDs relacionados:** RT-08, ADR-14, DT-03.

## DT-08: técnicas dos testes de integração das rotas de tarefa

- **Data e *release*:** 05/10/2026, `v0.3.0`.
- **Contexto:** dois comportamentos são difíceis de provocar sem dublês frágeis: o `500` por falha inesperada do banco e a mudança de `updated_at`, que depende da resolução do relógio (no Windows com Python 3.11 duas leituras seguidas podem devolver o mesmo instante).
- **Decisão:** o `500` é provocado pela *fixture* `broken_db_client`, que liga o `get_db` a um banco em memória **sem** a tabela `tasks`; a falha (`no such table`) é real do SQLAlchemy e o teste confere o log e a ausência de SQL e de nome de tabela na resposta. A mudança de `updated_at` é verificada com `age_updated_at`, que grava antes um valor antigo fixo direto no banco (`2020-01-01`) e compara o resultado da alteração com esse valor.
- **Alternativas descartadas:** `FailingSession` nas rotas de tarefa, porque o *service* chama métodos da sessão que o dublê não implementa e o teste deixaria de exercitar o caminho real; `time.sleep` entre a criação e a alteração, porque deixa o teste lento e ainda dependente do relógio.
- **Consequências:** o teste do `500` depende da mensagem `no such table` do SQLite; se o SQLAlchemy ou o SQLite mudarem o texto, o teste precisa ser ajustado. A *fixture* `broken_db_client` descarta o próprio *engine* em `engine.dispose()`.
- **IDs relacionados:** RT-09, RNF-10, ADR-06, DT-03.
