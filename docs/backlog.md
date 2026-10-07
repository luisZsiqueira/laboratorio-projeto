# Backlog do MVP

> **Status:** backlog criado após a *release* `v0.1.0`; itens da `v0.2.0` concluídos em 05/10/2026 e da `v0.3.0` em 06/10/2026. É revisado no *blueprint* e no fechamento de cada *release*: itens concluídos são marcados, e itens novos só entram com decisão do autor.

O backlog organiza por *release* o trabalho que falta para entregar o MVP descrito em [`docs/escopo-mvp.md`](escopo-mvp.md). Os requisitos são definidos lá; aqui eles viram itens executáveis, com critérios de aceite verificáveis por teste ou por inspeção.

## 1. Convenções

| Prefixo | Significado | Origem |
| --- | --- | --- |
| `RF-NN` | requisito funcional: comportamento observável da API | mesmo ID de [`docs/escopo-mvp.md`](escopo-mvp.md) (seção 3) |
| `RT-NN` | requisito técnico: infraestrutura, código interno, testes, documentação ou publicação necessários para entregar os RF e atender aos requisitos não funcionais (RNF) | criado neste backlog; cada item indica os RNF que atende |

- **Critérios de aceite** são numerados e verificáveis. O sufixo indica como: **[T]** teste automatizado (com o arquivo de teste), **[I]** inspeção de código ou de documentação, **[C]** execução de comando.
- **Estimativa** em horas, incluindo testes e documentação do item. É uma ordem de grandeza para controle do orçamento, não um compromisso.
- **Situação:** `a fazer`, `em andamento`, `concluído` ou `bloqueado` (com o motivo).
- Itens que dependem de uma decisão em aberto (D-NN, seção 6 do escopo) indicam a decisão; ela é tomada no *blueprint* da *release*, antes do código.
- Arquivos citados seguem a estrutura de diretórios do [`CLAUDE.md`](../CLAUDE.md).

## 2. Critérios comuns a todos os itens

Valem para todo item, além dos critérios próprios, e não são repetidos nas tabelas:

1. A definição de pronto passa sem avisos: `python -m pytest -W error` **[C]**. Até a `v0.4.0` incluía `python -m mypy --explicit-package-bases app`, retirado em 07/10/2026 (ADR-21).
2. Código com *type hints*, *docstrings* em português e conjuntos fechados com `typing.Literal` **[I]**.
3. Camadas respeitadas: rotas sem acesso ao banco nem regra de negócio, *service* sem HTTP, *repository* sem regra de negócio **[I]**.
4. Nenhum padrão proibido no roteiro de checagem de APIs deprecadas do `CLAUDE.md` **[I]**.
5. Uso de IA registrado no arquivo do *prompt* e em `docs/HISTORY-IA.md` **[I]**.

### 2.1 Fechamento de cada *release*

Executado ao final de cada *release*, conforme o `CLAUDE.md` (Fechamento de release):

1. README revisado por inteiro e descrevendo o projeto como ele está; roadmap atualizado **[I]**.
2. `docs/arquitetura.md` ajustado no que a implementação divergiu **[I]**.
3. `CHANGELOG.md` com a seção da *release*, agrupada por tipo de *commit* **[I]**.
4. Itens deste backlog marcados como `concluído` ou movidos, com justificativa **[I]**.
5. *Merge* `--no-ff` em `main`, *tag* anotada `vX.Y.Z` publicada com autorização **[C]**.
6. Definição de pronto executada em clone limpo **[C]**.

## 3. Resumo

| *Release* | Objetivo | Itens | Estimativa | Horas reais |
| --- | --- | --- | --- | --- |
| `v0.2.0` | base técnica: configuração, banco, aplicação, `/health` | RT-01 a RT-04, RF-12, RF-13 | 4 h | 4 h |
| `v0.3.0` | CRUD de tarefas | RT-05 a RT-09, RF-01 a RF-08 | 6,5 h | 8 h |
| `v0.4.0` | prioridades e `priority_advisor`, filtro por prioridade e datas no horário local | RT-10, RF-09 a RF-11, RF-14; D-09 | 5,75 h | 3 h |
| `v0.5.0` | revisão de arquitetura, segurança e documentação | RT-11 a RT-14 | 2,5 h | — |
| `v1.0.0` | entrega do curso | RT-15 a RT-17 | 2 h | — |
| **Total** | | 17 RT, 14 RF | **20,75 h** | **15 h** (até a `v0.4.0`) |

As horas reais são informadas pelo autor por *release*, e não por item. Elas incluem o *blueprint*, o fechamento e o *git*, que as estimativas por item não cobrem. O tempo da `v0.1.0` (inicialização e documentação) não foi medido. Até a `v0.3.0`, foram gastas 12 h contra 10,5 h estimadas. Na `v0.4.0`, a estimativa passou de 3,5 h para 5,75 h com o RF-14 (0,5 h) e a D-09 (1,75 h), aprovados no *blueprint*; com o *blueprint* e o fechamento, a *release* foi estimada em 7,25 h. As horas reais da `v0.4.0` foram 3 h, abaixo da estimativa, e até a `v0.4.0` foram gastas 15 h contra 16,75 h estimadas. Somadas as estimativas das *releases* restantes, com *blueprint* e fechamento (`v0.5.0`: 4 h; `v1.0.0`: 3 h), a projeção é de cerca de 22 h, dentro do orçamento de cerca de 30 horas. A comparação é refeita no fechamento de cada *release*.

## 4. Backlog por *release*

### 4.1 `v0.2.0`: base técnica

Decisão do *blueprint*: D-08 (esquema da resposta de `/health`), tomada em [`docs/blueprint-v020.md`](blueprint-v020.md) e registrada no ADR-13.

**Situação da *release*:** concluída em 05/10/2026. Os seis itens foram entregues como planejados, sem item movido. Horas reais (informadas pelo autor em 06/10/2026): 4 h para a *release* inteira, iguais à estimativa, que não incluía *blueprint* e fechamento. Não há medição por item.

| ID | Item | Critérios de aceite | Atende | Est. | Situação |
| --- | --- | --- | --- | --- | --- |
| RT-01 | Configuração por ambiente em `app/models/settings.py` (pydantic-settings) | 1. `DATABASE_URL` e `ENVIRONMENT` lidas do ambiente ou do `.env`, com os padrões do README (Configuração) **[T]** `test_task_routes.py`<br>2. `ENVIRONMENT` tipada com `Literal["development", "test", "production"]`; valor fora do conjunto impede a inicialização **[T]**<br>3. Uso de `SettingsConfigDict`, sem `class Config` **[I]**<br>4. Nenhum literal de configuração fora de `settings.py` **[I]** | RNF-07 | 0,5 h | concluído (05/10/2026) |
| RT-02 | Base declarativa e acesso ao banco em `app/models/base.py` e `app/repositories/database.py` | 1. `class Base(DeclarativeBase)` em `base.py` (ADR-02) **[I]**<br>2. *Engine* criada a partir de `DATABASE_URL`, com `check_same_thread=False` (ADR-04) **[I]**<br>3. `get_db` abre uma sessão por requisição e a fecha ao final, inclusive em caso de erro **[T]**<br>4. `ping(session)` executa `SELECT 1` via `text()` e devolve `False` em `SQLAlchemyError`, registrando o detalhe no log (ADR-07) **[T]** | RNF-09, RNF-12 | 1 h | concluído (05/10/2026) |
| RT-03 | Composição da aplicação em `app/main.py` | 1. `FastAPI(lifespan=...)` com `@asynccontextmanager`; sem `on_event` (ADR-05) **[I]**<br>2. Tabelas criadas com `Base.metadata.create_all` no `lifespan` **[T]**<br>3. `main.py` contém só criação da aplicação, `lifespan` e registro das rotas **[I]**<br>4. `python -m uvicorn app.main:app --reload` sobe a API a partir da raiz **[C]** | RNF-06 | 0,5 h | concluído (05/10/2026) |
| RT-04 | Infraestrutura de testes de integração em `tests/test_task_routes.py` | 1. Fixture com `sqlite://` e `StaticPool`, substituindo `get_db` por `dependency_overrides` (ADR-06) **[I]**<br>2. Fixture chama `engine.dispose()` e limpa os *overrides* ao final; nenhum `ResourceWarning` com `-W error` **[C]**<br>3. `TestClient` usando `httpx2`, sem aviso de deprecação (ADR-09) **[C]**<br>4. Testes não criam arquivos no repositório **[C]** `git status` limpo após os testes | RNF-03, RNF-04 | 1 h | concluído (05/10/2026) |
| RF-12 | Verificar saúde: `GET /health` | 1. Banco disponível: **200** com corpo JSON indicando aplicação e banco saudáveis **[T]** `test_task_routes.py`<br>2. Banco indisponível (`ping` falha): **503** com corpo JSON genérico, sem SQL, caminho nem *stack trace* **[T]**<br>3. Fluxo `health_routes` → `health_service` → `database.ping` (ADR-07) **[I]**<br>4. Corpo da resposta definido por esquema Pydantic, no arquivo decidido em D-08 **[I]** | RNF-10, RNF-12 | 0,5 h | concluído (05/10/2026) |
| RF-13 | Documentação interativa conforme o ambiente | 1. Com `ENVIRONMENT=development`, `/docs` e `/openapi.json` respondem **200** **[T]** `test_task_routes.py`<br>2. Com `ENVIRONMENT=production`, `/docs`, `/redoc` e `/openapi.json` respondem **404** (ADR-08) **[T]** | RNF-10 | 0,5 h | concluído (05/10/2026) |

### 4.2 `v0.3.0`: CRUD de tarefas

Decisões do *blueprint*: D-01 (valores de `TaskStatus`), D-02 (rota de conclusão), D-03 (coluna `priority` já nesta *release*) e D-04 (prioridade padrão), tomadas em [`docs/blueprint-v030.md`](blueprint-v030.md) com a recomendação do escopo e registradas nos requisitos e no ADR-15. O *blueprint* também criou o ADR-14 e as DT-04 a DT-08.

**Situação da *release*:** concluída em 06/10/2026. Os treze itens foram entregues como planejados, sem item movido. O código foi executado em 05/10/2026 (Prompts 26 a 29), e os exemplos do README e o fechamento em 06/10/2026 (Prompts 30 e 31). Horas reais (informadas pelo autor em 06/10/2026): 8 h para a *release* inteira, contra 6,5 h estimadas. Segundo o autor, o trabalho em si caberia em 3 a 4 h. O excedente veio de falhas repetidas de conexão com a API do Claude, causadas pelo uso de internet por *hotspot* compartilhado do celular, que forçaram retomadas da execução. Não há medição por item.

| ID | Item | Critérios de aceite | Atende | Est. | Situação |
| --- | --- | --- | --- | --- | --- |
| RT-05 | Modelo ORM `Task` em `app/models/task.py` | 1. Colunas e restrições conforme o modelo de dados de `docs/arquitetura.md` e o escopo (seção 2.1), com `Mapped`/`mapped_column` **[I]**<br>2. `created_at` e `updated_at` preenchidos em UTC; `updated_at` muda a cada alteração **[T]** `test_task_routes.py`<br>3. Datas lidas do SQLite voltam *timezone-aware* em UTC (ADR-10) **[T]** | RNF-11 | 1 h | concluído (06/10/2026) |
| RT-06 | Esquemas Pydantic em `app/models/task_schemas.py` | 1. `TaskStatus` e `TaskPriority` como `Literal` **[I]**<br>2. Esquemas de criação, atualização total, atualização parcial e leitura, com `title` de 1 a 200 e `description` até 1000 caracteres **[T]**<br>3. Leitura a partir do ORM com `ConfigDict(from_attributes=True)`, sem `class Config` **[I]**<br>4. Campos somente leitura (`id`, `created_at`, `updated_at`) rejeitados na entrada com **422** (`extra="forbid"`, ADR-15) **[T]** | RNF-05, RNF-08 | 1 h | concluído (06/10/2026) |
| RT-07 | *Repository* em `app/repositories/task_repository.py` | 1. Operações de inserir, buscar por `id`, listar (com filtro opcional), atualizar e excluir **[T]** via rotas<br>2. Só ORM ou `text()` com parâmetros nomeados; nenhuma concatenação de SQL **[I]**<br>3. Sem regra de negócio **[I]**<br>4. Escritas confirmadas com `commit` seguido de `refresh` no *repository*; `get_db` não faz `commit` (ADR-12) **[T]** via rotas | RNF-09 | 0,5 h | concluído (06/10/2026) |
| RT-08 | *Service* em `app/services/task_service.py` | 1. Casos de uso de criar, listar, consultar, atualizar (total e parcial), concluir e excluir **[T]** `test_task_service.py`<br>2. Tarefa inexistente sinalizada por exceção de domínio, sem código HTTP **[T]**<br>3. Testes unitários isolam o *repository* com um dublê simples, sem banco **[I]** | RNF-03, RNF-06 | 1 h | concluído (06/10/2026) |
| RT-09 | Tratamento de erros e exemplos de uso | 1. Exceção de domínio traduzida para **404** na rota **[T]** `test_task_routes.py`<br>2. Falha inesperada do banco responde **500** com mensagem genérica; detalhe no log **[T]**<br>3. README (Endpoints) com a tabela de endpoints, códigos de resposta e exemplos de requisição e resposta para cada um **[I]** | RNF-10, RNF-13 | 1 h | concluído (06/10/2026) |
| RF-01 | Criar tarefa: `POST /tasks` | 1. Corpo válido: **201** com `id`, `created_at`, `updated_at` e *status*/prioridade padrão **[T]** `test_task_routes.py`<br>2. Título vazio ou acima de 200, descrição acima de 1000, *status* ou prioridade fora do conjunto, data/hora mal formada: **422** **[T]** | — | 0,5 h | concluído (06/10/2026) |
| RF-02 | Listar tarefas: `GET /tasks` | 1. Sem tarefas: **200** com lista vazia **[T]**<br>2. Com tarefas: **200** com todas elas **[T]** | — | 0,25 h | concluído (06/10/2026) |
| RF-03 | Filtrar por *status*: `GET /tasks?status=` | 1. Devolve só as tarefas com o *status* pedido **[T]**<br>2. Valor fora do conjunto: **422** **[T]** | — | 0,25 h | concluído (06/10/2026) |
| RF-04 | Consultar tarefa: `GET /tasks/{id}` | 1. Existente: **200** com a tarefa **[T]**<br>2. Inexistente: **404** **[T]** | — | 0,25 h | concluído (06/10/2026) |
| RF-05 | Atualizar (total): `PUT /tasks/{id}` | 1. Corpo completo válido: **200**, campos substituídos e `updated_at` alterado **[T]**<br>2. Inexistente: **404**; corpo inválido ou incompleto: **422** **[T]** | — | 0,25 h | concluído (06/10/2026) |
| RF-06 | Atualizar (parcial): `PATCH /tasks/{id}` | 1. Só os campos enviados mudam; os demais permanecem **[T]**<br>2. Inexistente: **404**; campo inválido: **422** **[T]** | — | 0,25 h | concluído (06/10/2026) |
| RF-07 | Marcar como concluída: `POST /tasks/{id}/complete` (D-02) | 1. Existente: **200** com *status* `done` **[T]**<br>2. Repetir a operação mantém o *status* e `updated_at` e responde **200** (idempotente, D-02) **[T]**<br>3. Inexistente: **404** **[T]** | — | 0,25 h | concluído (06/10/2026) |
| RF-08 | Excluir tarefa: `DELETE /tasks/{id}` | 1. Existente: **204** sem corpo; consulta posterior responde **404** **[T]**<br>2. Inexistente: **404** **[T]** | — | 0,25 h | concluído (06/10/2026) |

### 4.3 `v0.4.0`: prioridades e `priority_advisor`

Decisões do *blueprint* ([`docs/blueprint-v040.md`](blueprint-v040.md)): D-05 (prioridade 4 exige `due_at`), D-06 (filtro por prioridade incluído como RF-14), D-07 (coerência na criação e na atualização; sugestão em `suggested_priority`, sem gravar) e D-09 (datas no horário local, pedida pelo autor na revisão do *blueprint*).

**Situação da *release*:** concluída em 06/10/2026. Os quatro itens planejados foram entregues, mais o RF-14 e a D-09, aprovados no *blueprint*; nenhum item foi movido. O código foi executado nos Prompts 33 e 34 e o fechamento no Prompt 35. Horas reais (informadas pelo autor em 06/10/2026): 3 h para a *release* inteira, contra 5,75 h estimadas para os itens e 7,25 h com *blueprint* e fechamento. Não há medição por item.

| ID | Item | Critérios de aceite | Atende | Est. | Situação |
| --- | --- | --- | --- | --- | --- |
| RT-10 | `app/services/priority_advisor.py` com funções puras | 1. Não importa banco, *repository* nem HTTP **[I]**<br>2. Recebe a data/hora de referência como parâmetro, para testes determinísticos **[I]**<br>3. Testes unitários de cada regra, incluindo os limites **[T]** `test_priority_advisor.py` | RNF-03, RNF-06 | 1 h | concluído (06/10/2026) |
| RF-09 | Prioridade e tipo da tarefa | 1. Prioridade de 1 a 4 aceita na criação e na atualização; fora do conjunto: **422** **[T]** `test_task_routes.py`<br>2. Tarefa sem `due_at` (aberta) e com `due_at` (específica) persistidas e devolvidas corretamente **[T]**<br>3. Critério substituído pela D-09: (a) `DD/MM/AAAA HH:MM` gravado como horário local **[T]**; (b) `DD/MM/AAAA` gravado como 23:59 local, no `POST` e no `PATCH` **[T]**; (c) formatos fora dos três aceitos respondem **422** **[T]**; (d) as datas da resposta vêm no deslocamento de `LOCAL_UTC_OFFSET` **[T]**; (e) `LOCAL_UTC_OFFSET` fora de `±HH:MM` impede a partida **[T]** | RNF-11 | 0,5 h (+ 1,75 h da D-09) | concluído (06/10/2026) |
| RF-10 | Validar coerência de prioridade | 1. Combinação incoerente, conforme D-05, responde **422** com mensagem clara na criação, no `PUT` e no `PATCH` **[T]** `test_task_routes.py`<br>2. A regra é aplicada pelo *service* chamando o `priority_advisor` **[T]** `test_task_service.py` | — | 1 h | concluído (06/10/2026) |
| RF-11 | Sugerir prioridade | 1. Sugestão determinística pela proximidade do prazo, exposta conforme D-07 **[T]** `test_priority_advisor.py` e `test_task_routes.py`<br>2. A sugestão não altera a prioridade gravada **[T]** | — | 1 h | concluído (06/10/2026) |
| RF-14 | Filtrar a listagem por prioridade (D-06) | 1. `?priority=` devolve só as tarefas com aquela prioridade **[T]** `test_task_routes.py`<br>2. Combinado com `?status=`, devolve as que atendem aos dois **[T]**<br>3. Valor fora de 1 a 4 ou não inteiro responde **422** **[T]** | RNF-08 | 0,5 h | concluído (06/10/2026) |

### 4.4 `v0.5.0`: revisão

| ID | Item | Critérios de aceite | Atende | Est. | Situação |
| --- | --- | --- | --- | --- | --- |
| RT-11 | Revisão de arquitetura | 1. Importações conferidas contra o diagrama de módulos de `docs/arquitetura.md`; nenhuma dependência para cima **[I]**<br>2. Divergências corrigidas no código ou registradas em `docs/arquitetura.md` (ajuste pontual ou novo ADR) **[I]** | RNF-06 | 0,5 h | a fazer |
| RT-12 | Revisão de segurança | 1. Nenhum SQL montado por concatenação ou *f-string* **[I]**<br>2. Respostas de erro (404, 422, 500, 503) sem detalhes internos **[T]**<br>3. Varredura de segredos no repositório e no histórico **[C]**<br>4. Documentação desabilitada em produção confirmada **[T]** | RNF-08, RNF-09, RNF-10 | 1 h | a fazer |
| RT-13 | Revisão da documentação | 1. README conferido contra o comportamento real da API: endpoints, códigos e exemplos executados **[C]**<br>2. *Docstrings* presentes em todas as classes e funções públicas **[I]**<br>3. `docs/escopo-mvp.md` sem decisões em aberto pendentes **[I]** | RNF-13 | 0,5 h | a fazer |
| RT-14 | Nova rodada do roteiro de checagem de APIs deprecadas | 1. Versões do `requirements.txt` conferidas com o PyPI, com data **[C]**<br>2. Se alguma versão mudar: notas de versão lidas, testes mínimos executados e tabela do `CLAUDE.md` atualizada **[C]**<br>3. `python -m pip check` sem conflitos **[C]** | RNF-02, RNF-04 | 0,5 h | a fazer |

### 4.5 `v1.0.0`: entrega do curso

| ID | Item | Critérios de aceite | Atende | Est. | Situação |
| --- | --- | --- | --- | --- | --- |
| RT-15 | Validação em máquina limpa | 1. Clone novo, `.venv` novo e instalação só com os comandos do README **[C]**<br>2. API sobe e responde em `/health` e nos exemplos do README **[C]**<br>3. Definição de pronto passa no clone **[C]**<br>4. Execução feita em PowerShell; Bash conferido no Git Bash ou registrado como não verificado **[C]** | RNF-01, RNF-02 | 0,75 h | a fazer |
| RT-16 | Histórico de uso de IA consolidado | 1. `docs/HISTORY-IA.md` com todas as entradas, consolidação por *release* e análise final **[I]**<br>2. README (Uso de IA generativa) lista todos os assistentes, modelos e etapas **[I]**<br>3. Todo *prompt* de `prompts/` tem o registro da execução **[I]** | RNF-15 | 0,75 h | a fazer |
| RT-17 | Publicação da entrega | 1. Rastreabilidade com os requisitos do curso (seção 7 do escopo) toda como atendida **[I]**<br>2. Status do README como "concluído" na `v1.0.0` **[I]**<br>3. *Tag* `v1.0.0` publicada e *Release* criada no GitHub com o texto do `CHANGELOG.md` **[C]** | RNF-14 | 0,5 h | a fazer |

## 5. Rastreabilidade dos requisitos não funcionais

| RNF | Coberto por |
| --- | --- |
| RNF-01 Reprodutibilidade | RT-15; fechamento de cada *release* (2.1, item 6) |
| RNF-02 Dependências | RT-14, RT-15 |
| RNF-03 Testabilidade | RT-04, RT-08, RT-10; critérios **[T]** de todos os RF |
| RNF-04 Ausência de avisos | RT-04, RT-14; critério comum 1 |
| RNF-05 Tipagem | RT-06; critérios comuns 1 e 2 |
| RNF-06 Arquitetura | RT-03, RT-08, RT-10, RT-11; critério comum 3 |
| RNF-07 Configuração | RT-01 |
| RNF-08 Entrada | RT-06, RT-12 |
| RNF-09 Banco | RT-02, RT-07, RT-12 |
| RNF-10 Exposição | RF-12, RF-13, RT-09, RT-12 |
| RNF-11 Datas | RT-05, RF-09 |
| RNF-12 Observabilidade | RT-02, RF-12 |
| RNF-13 Documentação | RT-09, RT-13; fechamento de cada *release* |
| RNF-14 Versionamento | RT-17; fechamento de cada *release* |
| RNF-15 Uso de IA | RT-16; critério comum 5 |
