# laboratorio-projeto: micro-API de gestão de tarefas

> **Status:** concluído. Entregue na `v1.0.0` (07/10/2026), com *tag* e *Release* no GitHub. A API implementa todos os requisitos funcionais do escopo: criar, listar com filtros por *status* e prioridade, consultar, atualizar, concluir e excluir tarefas, com a coerência entre prioridade e prazo validada, uma prioridade sugerida pela proximidade do prazo e datas no horário local, além do `GET /health` com consulta real ao banco. São 143 testes automatizados, que passam com `python -m pytest -W error`. A instalação, a execução e os testes foram validados num clone limpo, só com os comandos deste README, em PowerShell e em Git Bash. O caminho percorrido está no Roadmap, e as mudanças de cada *release*, no [`CHANGELOG.md`](CHANGELOG.md).

Micro-API REST de gestão de tarefas (*To-Do List*) com prioridades, em Python, FastAPI e SQLite3. É o miniprojeto acadêmico do curso 1 da pós-graduação SWE-GENAI, que exige o uso de IA generativa em todo o ciclo de vida do software.

## Objetivo

Entregar um MVP pequeno, claro, funcional, bem testado e bem documentado, que um avaliador consiga clonar, instalar, executar e testar em uma máquina limpa.

### Escopo do MVP

- Criar, listar (com filtros por *status* e por prioridade), consultar, atualizar (total e parcial), marcar como concluída e excluir tarefas.
- Cada tarefa tem uma prioridade e pode ser **aberta** (sem data/hora) ou **específica** (com data/hora estipulada), informada no horário local (`DD/MM/AAAA HH:MM` ou só `DD/MM/AAAA`).
- *Health check* real da aplicação e do banco de dados (`/health`).
- Assessor de prioridade (`priority_advisor`) com regras determinísticas, sem IA: recusa a prioridade `4` (agendada) sem data/hora e sugere uma prioridade pela proximidade do prazo, devolvida em `suggested_priority` sem alterar a prioridade gravada (ver [Sugestão de prioridade](#sugestão-de-prioridade)).

Os requisitos funcionais e não funcionais, com critérios de aceitação, os itens fora de escopo e as decisões em aberto estão em [`docs/escopo-mvp.md`](docs/escopo-mvp.md).

### Prioridades

| Valor | Significado |
| --- | --- |
| 1 | Mandatória: fazer imediatamente |
| 2 | Importante: fazer hoje, se possível |
| 3 | Regular: fazer quando houver tempo |
| 4 | Agendada: fazer na data/hora estipulada |

Sem prioridade informada, a tarefa é criada com prioridade `3`. A prioridade `4` exige `due_at`; `due_at` não exige prioridade `4`.

#### Sugestão de prioridade

Toda resposta de tarefa traz `suggested_priority`, calculada pela proximidade do prazo (`due_at` menos o instante atual). É só uma sugestão: nunca é gravada e não altera a `priority` da tarefa. Os limites pertencem à faixa mais urgente.

| Situação | Tempo restante | `suggested_priority` |
| --- | --- | --- |
| tarefa concluída (`status` `done`) | qualquer | `null` |
| tarefa aberta (`due_at` nulo) | não se aplica | `null` |
| prazo vencido ou próximo | até 4 h (inclui prazo vencido) | `1` (mandatória) |
| prazo no dia | mais de 4 h, até 24 h | `2` (importante) |
| prazo na semana | mais de 24 h, até 7 dias | `3` (regular) |
| prazo distante | mais de 7 dias | `4` (agendada) |

## Stack

| Componente | Versão | Uso |
| --- | --- | --- |
| Python | 3.11+ (testado em 3.14.6) | linguagem |
| FastAPI | 0.142.2 | framework web e documentação OpenAPI |
| Starlette | 1.7.0 | base do FastAPI (dependência transitiva) |
| Uvicorn | 0.54.0 | servidor ASGI |
| SQLAlchemy | 2.1.3 | ORM (`Mapped` / `mapped_column`) |
| Pydantic | 2.13.5 | validação de dados |
| pydantic-settings | 2.15.0 | configuração por variáveis de ambiente |
| SQLite3 | embutido no Python | banco de dados |
| pytest | 9.1.1 | testes unitários e de integração |
| httpx2 | 2.13.1 | cliente HTTP do `TestClient` |
| Mermaid.js | renderizado pelo GitHub | diagramas de arquitetura |

As versões estão fixadas no [`requirements.txt`](requirements.txt), incluindo as dependências transitivas. Elas foram consultadas no PyPI em 03/10/2026 e conferidas de novo em 07/10/2026, na revisão da `v0.5.0`: sem vulnerabilidade publicada e sem conflito no `pip check`; as versões mais novas do FastAPI (0.142.3) e do SQLAlchemy (2.1.4), publicadas no mesmo dia, não foram adotadas, porque não corrigem defeito que afete o projeto. O Python 3.11 é o mínimo porque o SQLAlchemy 2.1 o exige.

## Arquitetura

API síncrona em camadas, uma por pacote em `app/`:

```mermaid
flowchart LR
    C(["Cliente HTTP"]) --> API["app/api<br/>rotas"]
    API --> SVC["app/services<br/>regras de negócio"]
    SVC --> REPO["app/repositories<br/>acesso ao banco"]
    REPO --> DB[("SQLite3")]
    MOD["app/models<br/>ORM, esquemas, settings"] -.-> API
    MOD -.-> SVC
    MOD -.-> REPO
```

Os módulos e suas dependências, o fluxo de dados de `POST /tasks` (com o `priority_advisor`), `GET /health` e dos erros em `/tasks/{id}`, o modelo de dados, a estratégia de testes e as decisões de arquitetura (ADRs) estão em [`docs/arquitetura.md`](docs/arquitetura.md). O histórico visual dos diagramas, com o antes e o depois de cada revisão, está em [`docs/mermaid.md`](docs/mermaid.md).

## Endpoints

Com a API em execução (ver [Como rodar localmente](#como-rodar-localmente)), todos os endpoints respondem em `http://127.0.0.1:8000` e trocam JSON. A documentação interativa gerada pelo FastAPI fica em `/docs`.

| Método e caminho | Descrição | Respostas |
| --- | --- | --- |
| `POST /tasks` | cria uma tarefa; prioridade `4` exige `due_at` | `201` criada; `422` corpo inválido ou prioridade incoerente |
| `GET /tasks` | lista as tarefas por `id`; filtros opcionais `?status=pending` ou `?status=done` e `?priority=1` a `4`, combináveis (`?status=done&priority=1`) | `200`; `422` *status* ou prioridade inválidos |
| `GET /tasks/{id}` | consulta uma tarefa | `200`; `404` não existe; `422` `id` não numérico ou acima de 9223372036854775807 |
| `PUT /tasks/{id}` | substitui os cinco campos editáveis (todos obrigatórios) | `200`; `404`; `422` corpo inválido ou prioridade incoerente |
| `PATCH /tasks/{id}` | altera só os campos enviados; a coerência entre prioridade e `due_at` vale para o estado resultante | `200`; `404`; `422` corpo inválido ou prioridade incoerente |
| `POST /tasks/{id}/complete` | marca como concluída; repetir a chamada é permitido e devolve a mesma tarefa | `200`; `404`; `422` |
| `DELETE /tasks/{id}` | exclui a tarefa | `204` sem corpo; `404`; `422` |
| `GET /health` | verifica a aplicação e o banco de dados, com uma consulta real (`SELECT 1`) | `200` banco disponível; `503` banco indisponível |
| `GET /docs`, `GET /redoc`, `GET /openapi.json` | documentação interativa e esquema OpenAPI | `200` em `development` e `test`; `404` em `production` |

Qualquer endpoint de `/tasks` responde `500` com `{"detail": "Erro interno do servidor"}` se o banco falhar de forma inesperada; a causa vai para o log, nunca para a resposta.

### Tarefa

| Campo | Tipo | Em `POST` | Observação |
| --- | --- | --- | --- |
| `id` | inteiro | somente leitura | gerado pela API |
| `title` | texto, 1 a 200 caracteres | obrigatório | espaços nas pontas são removidos; título vazio ou só com espaços é rejeitado |
| `description` | texto de até 1000 caracteres, ou `null` | opcional | padrão `null` |
| `status` | `pending` ou `done` | opcional | padrão `pending` |
| `priority` | `1`, `2`, `3` ou `4` | opcional | padrão `3`; significados em [Prioridades](#prioridades) |
| `due_at` | data e hora em um dos três formatos abaixo, ou `null` | opcional | `null` é tarefa aberta; com valor, é tarefa específica. Obrigatório quando `priority` é `4` |
| `created_at`, `updated_at` | data e hora ISO 8601 no fuso local | somente leitura | gerados pela API |
| `suggested_priority` | `1`, `2`, `3`, `4` ou `null` | somente leitura | calculada a cada resposta pela proximidade do prazo, nunca gravada; `null` para tarefa aberta ou concluída (ver [Sugestão de prioridade](#sugestão-de-prioridade)) |

Formatos aceitos em `due_at` (entrada em `POST`, `PUT` e `PATCH`):

| Formato | Exemplo | Valor gravado |
| --- | --- | --- |
| `DD/MM/AAAA HH:MM`, horário local | `"20/10/2026 14:30"` | 14:30 no fuso local |
| `DD/MM/AAAA`, horário local | `"20/10/2026"` | 23:59 do dia, no fuso local (só o dia vale até o fim do dia) |
| ISO 8601 **com** fuso horário, para programas | `"2026-10-20T17:30:00Z"` | o mesmo instante, convertido |

Qualquer outro formato responde `422`, inclusive ISO só com a data (`"2026-10-20"`), ISO sem fuso, data inexistente (`"31/02/2026"`), ano com dois dígitos e hora sem os minutos. O banco guarda as datas em UTC; `due_at`, `created_at` e `updated_at` são devolvidos no fuso local, em ISO 8601 (`2026-10-20T23:59:00-03:00`), e o fuso é configurado em `LOCAL_UTC_OFFSET` (ver [Configuração](#configuração)). A API não registra se só o dia foi informado: a resposta mostra 23:59.

Campos desconhecidos ou somente leitura no corpo (`id`, `created_at`, `updated_at`, `suggested_priority`) são rejeitados com `422`. No `PATCH`, `title`, `status` e `priority` não aceitam `null`; `description` e `due_at` aceitam `null` para limpar o valor.

### Erros

| Código | Quando | Corpo |
| --- | --- | --- |
| `404` | tarefa inexistente | `{"detail": "Tarefa não encontrada"}` |
| `422` | corpo, parâmetro de consulta ou `id` fora das regras de validação | `{"detail": [...]}`, uma entrada por campo inválido, com `loc` (onde), `msg` (o quê) e `input` (o valor recebido) |
| `422` | prioridade `4` sem `due_at` (`POST`, `PUT`, `PATCH`) | `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`, em texto e não em lista |
| `500` | falha inesperada do banco | `{"detail": "Erro interno do servidor"}` |

### Exemplos de uso

Os exemplos foram executados contra a API em execução em 06/10/2026 e de novo em 07/10/2026, no Windows PowerShell 5.1, com os mesmos códigos e corpos, com o banco vazio e `LOCAL_UTC_OFFSET` no padrão (`-03:00`), na ordem da seção, exceto os exemplos de prioridade 4, de `422` por coerência e de filtro por prioridade, executados no fim, com a tarefa 1 concluída e a tarefa de `id` 2 excluída (a que eles criam recebe o `id` 2). Os JSON mostrados são as respostas reais; o `id`, os instantes (`created_at`, `updated_at`) e a `suggested_priority` do seu teste serão outros, pois dependem do momento da execução. Em Bash, `curl -i` mostra a linha de *status*. Em PowerShell, `Invoke-RestMethod` converte o JSON da resposta em objeto; o texto JSON abaixo é o corpo enviado pela API.

Em PowerShell, `Invoke-RestMethod` lança exceção nas respostas de erro (`404`, `422`). Para ver o código e o corpo, use `try`/`catch`, como nos exemplos de erro abaixo (verificado no Windows PowerShell 5.1).

Os exemplos usam títulos sem acento. No Git Bash do Windows, `curl -d` com caracteres não ASCII na linha de comando foi rejeitado com `400 Bad Request` nesta máquina (página de código 850); enviar o corpo de um arquivo UTF-8 com `--data-binary @tarefa.json` funcionou.

#### `POST /tasks`: criar tarefa

Tarefa específica, com prazo no horário local (`DD/MM/AAAA HH:MM`) e prioridade. O prazo volta no fuso local e a resposta traz `suggested_priority`: faltam mais de 7 dias, então a sugestão é `4`, mesmo com a prioridade `2` escolhida.

PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks -ContentType "application/json" -Body '{"title": "Entregar relatorio", "description": "Versao final em PDF", "priority": 2, "due_at": "20/10/2026 18:00"}'
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Entregar relatorio", "description": "Versao final em PDF", "priority": 2, "due_at": "20/10/2026 18:00"}'
```

`201 Created`:

```json
{"id":1,"title":"Entregar relatorio","description":"Versao final em PDF","status":"pending","priority":2,"due_at":"2026-10-20T18:00:00-03:00","created_at":"2026-10-06T17:22:31.288022-03:00","updated_at":"2026-10-06T17:22:31.288022-03:00","suggested_priority":4}
```

Tarefa aberta, só com o título (prioridade `3`, `pending` e `due_at: null` por padrão):

PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks -ContentType "application/json" -Body '{"title": "Estudar FastAPI"}'
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Estudar FastAPI"}'
```

`201 Created`:

```json
{"id":2,"title":"Estudar FastAPI","description":null,"status":"pending","priority":3,"due_at":null,"created_at":"2026-10-06T17:22:31.332243-03:00","updated_at":"2026-10-06T17:22:31.332243-03:00","suggested_priority":null}
```

**Caso `422`:** título só com espaços e prioridade fora de `1` a `4`.

PowerShell:

```powershell
try { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks -ContentType "application/json" -Body '{"title": "   ", "priority": 9}' } catch { [int]$_.Exception.Response.StatusCode; $_.ErrorDetails.Message }
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "   ", "priority": 9}'
```

`422 Unprocessable Content`:

```json
{"detail":[{"type":"string_too_short","loc":["body","title"],"msg":"String should have at least 1 character","input":"   ","ctx":{"min_length":1}},{"type":"literal_error","loc":["body","priority"],"msg":"Input should be 1, 2, 3 or 4","input":9,"ctx":{"expected":"1, 2, 3 or 4"}}]}
```

Tarefa agendada (prioridade `4`), só com o dia: o prazo vale até 23:59 do dia, no horário local.

PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks -ContentType "application/json" -Body '{"title": "Consulta no dentista", "priority": 4, "due_at": "20/10/2026"}'
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Consulta no dentista", "priority": 4, "due_at": "20/10/2026"}'
```

`201 Created`:

```json
{"id":2,"title":"Consulta no dentista","description":null,"status":"pending","priority":4,"due_at":"2026-10-20T23:59:00-03:00","created_at":"2026-10-06T17:22:36.475358-03:00","updated_at":"2026-10-06T17:22:36.475358-03:00","suggested_priority":4}
```

**Caso `422` de coerência:** prioridade `4` sem `due_at`. O corpo é um texto, e não a lista da validação.

PowerShell:

```powershell
try { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks -ContentType "application/json" -Body '{"title": "Sem data", "priority": 4}' } catch { [int]$_.Exception.Response.StatusCode; $_.ErrorDetails.Message }
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Sem data", "priority": 4}'
```

`422 Unprocessable Content`:

```json
{"detail":"Prioridade 4 (agendada) exige due_at preenchido"}
```

A mesma regra vale para `PUT` e `PATCH`, conferida no estado resultante: `PATCH {"due_at": null}` numa tarefa de prioridade `4` também responde `422` com esse corpo, e a tarefa não é alterada.

**Caso `422` de formato:** `due_at` em ISO só com a data não é aceito.

PowerShell:

```powershell
try { Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks -ContentType "application/json" -Body '{"title": "A", "due_at": "2026-10-20"}' } catch { [int]$_.Exception.Response.StatusCode; $_.ErrorDetails.Message }
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "A", "due_at": "2026-10-20"}'
```

`422 Unprocessable Content`, com uma entrada para cada formato tentado (ISO com fuso e `DD/MM/AAAA`):

```json
{"detail":[{"type":"timezone_aware","loc":["body","due_at","datetime"],"msg":"Input should have timezone info","input":"2026-10-20"},{"type":"value_error","loc":["body","due_at","function-before[parse_local_due_at(), datetime]"],"msg":"Value error, use DD/MM/AAAA HH:MM, DD/MM/AAAA ou ISO 8601 com fuso horário","input":"2026-10-20","ctx":{"error":{}}}]}
```

#### `GET /tasks`: listar tarefas

PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tasks
```

Bash:

```bash
curl -i http://127.0.0.1:8000/tasks
```

`200 OK`:

```json
[{"id":1,"title":"Entregar relatorio","description":"Versao final em PDF","status":"pending","priority":2,"due_at":"2026-10-20T18:00:00-03:00","created_at":"2026-10-06T17:22:31.288022-03:00","updated_at":"2026-10-06T17:22:31.288022-03:00","suggested_priority":4},{"id":2,"title":"Estudar FastAPI","description":null,"status":"pending","priority":3,"due_at":null,"created_at":"2026-10-06T17:22:31.332243-03:00","updated_at":"2026-10-06T17:22:31.332243-03:00","suggested_priority":null}]
```

Com filtro por *status*; nenhuma tarefa está concluída ainda, então a lista vem vazia:

PowerShell:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/tasks?status=done"
```

Bash:

```bash
curl -i "http://127.0.0.1:8000/tasks?status=done"
```

`200 OK`:

```json
[]
```

Um valor fora de `pending` e `done` (por exemplo, `?status=archived`) responde `422`:

```json
{"detail":[{"type":"literal_error","loc":["query","status"],"msg":"Input should be 'pending' or 'done'","input":"archived","ctx":{"expected":"'pending' or 'done'"}}]}
```

Com filtro por prioridade, depois de concluir a tarefa 1 e criar a tarefa de prioridade `4` acima (tarefas 1, `done`, prioridade `1`, e 2, `pending`, prioridade `4`):

PowerShell:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/tasks?priority=1"
```

Bash:

```bash
curl -i "http://127.0.0.1:8000/tasks?priority=1"
```

`200 OK`:

```json
[{"id":1,"title":"Entregar relatorio","description":null,"status":"done","priority":1,"due_at":"2026-10-20T18:00:00-03:00","created_at":"2026-10-06T17:22:31.288022-03:00","updated_at":"2026-10-06T17:22:31.673626-03:00","suggested_priority":null}]
```

Os filtros se combinam (E lógico). `?status=pending&priority=2` não encontra nenhuma tarefa e responde `200` com `[]`; `?status=done&priority=1` devolve a mesma tarefa 1 acima. Prioridade fora de `1` a `4` ou que não seja inteira (`?priority=5`, `?priority=alta`) responde `422`:

```json
{"detail":[{"type":"literal_error","loc":["query","priority"],"msg":"Input should be 1, 2, 3 or 4","input":5,"ctx":{"expected":"1, 2, 3 or 4"}}]}
```

#### `GET /tasks/{id}`: consultar tarefa

PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tasks/1
```

Bash:

```bash
curl -i http://127.0.0.1:8000/tasks/1
```

`200 OK`:

```json
{"id":1,"title":"Entregar relatorio","description":"Versao final em PDF","status":"pending","priority":2,"due_at":"2026-10-20T18:00:00-03:00","created_at":"2026-10-06T17:22:31.288022-03:00","updated_at":"2026-10-06T17:22:31.288022-03:00","suggested_priority":4}
```

**Caso `404`:** tarefa inexistente.

PowerShell:

```powershell
try { Invoke-RestMethod http://127.0.0.1:8000/tasks/999 } catch { [int]$_.Exception.Response.StatusCode; $_.ErrorDetails.Message }
```

Bash:

```bash
curl -i http://127.0.0.1:8000/tasks/999
```

`404 Not Found`:

```json
{"detail":"Tarefa não encontrada"}
```

#### `PUT /tasks/{id}`: substituir tarefa

Exige os cinco campos (`title`, `description`, `status`, `priority`, `due_at`), mesmo os que aceitam `null`.

PowerShell:

```powershell
Invoke-RestMethod -Method Put -Uri http://127.0.0.1:8000/tasks/2 -ContentType "application/json" -Body '{"title": "Estudar FastAPI e Pydantic", "description": null, "status": "pending", "priority": 1, "due_at": null}'
```

Bash:

```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/2 -H "Content-Type: application/json" -d '{"title": "Estudar FastAPI e Pydantic", "description": null, "status": "pending", "priority": 1, "due_at": null}'
```

`200 OK`; `updated_at` avança e `created_at` permanece (`suggested_priority` é `null`: tarefa sem prazo):

```json
{"id":2,"title":"Estudar FastAPI e Pydantic","description":null,"status":"pending","priority":1,"due_at":null,"created_at":"2026-10-06T17:22:31.332243-03:00","updated_at":"2026-10-06T17:22:31.578171-03:00","suggested_priority":null}
```

Enviar só `{"title": "Estudar FastAPI"}` responde `422` com uma entrada `missing` para cada um dos quatro campos ausentes (`description`, `status`, `priority`, `due_at`).

#### `PATCH /tasks/{id}`: alterar parcialmente

Altera a prioridade e limpa a descrição; os demais campos ficam como estão.

PowerShell:

```powershell
Invoke-RestMethod -Method Patch -Uri http://127.0.0.1:8000/tasks/1 -ContentType "application/json" -Body '{"priority": 1, "description": null}'
```

Bash:

```bash
curl -i -X PATCH http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"priority": 1, "description": null}'
```

`200 OK`:

```json
{"id":1,"title":"Entregar relatorio","description":null,"status":"pending","priority":1,"due_at":"2026-10-20T18:00:00-03:00","created_at":"2026-10-06T17:22:31.288022-03:00","updated_at":"2026-10-06T17:22:31.635977-03:00","suggested_priority":4}
```

Enviar `{"title": null}` responde `422` (`"msg":"Value error, o campo não aceita null"`).

#### `POST /tasks/{id}/complete`: concluir tarefa

Não tem corpo. Chamar de novo na tarefa já concluída responde `200` com a mesma tarefa, sem alterar `updated_at`.

PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/tasks/1/complete
```

Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks/1/complete
```

`200 OK` (`suggested_priority` é `null`: tarefa concluída):

```json
{"id":1,"title":"Entregar relatorio","description":null,"status":"done","priority":1,"due_at":"2026-10-20T18:00:00-03:00","created_at":"2026-10-06T17:22:31.288022-03:00","updated_at":"2026-10-06T17:22:31.673626-03:00","suggested_priority":null}
```

#### `DELETE /tasks/{id}`: excluir tarefa

PowerShell (a resposta `204` não tem corpo, então nada é exibido):

```powershell
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:8000/tasks/2
```

Bash:

```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/2
```

`204 No Content`, sem corpo. Repetir a chamada responde `404` com `{"detail":"Tarefa não encontrada"}`.

#### `GET /health`: saúde da aplicação e do banco

PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Bash:

```bash
curl -i http://127.0.0.1:8000/health
```

Banco disponível, `200 OK`:

```json
{"status":"ok","database":"ok"}
```

Banco indisponível, `503 Service Unavailable`:

```json
{"status": "unavailable", "database": "unavailable"}
```

O corpo do `503` não traz mensagem de erro, SQL nem *stack trace*; o detalhe da falha vai para o log da aplicação. Os campos `status` e `database` aceitam só `ok` e `unavailable` (ADR-13 em [`docs/arquitetura.md`](docs/arquitetura.md)). O exemplo do `503` não foi obtido da API em execução: reproduz o contrato exercitado nos testes de integração, que simulam o banco indisponível.

## Configuração

Toda configuração vem de variáveis de ambiente, opcionalmente lidas de um arquivo `.env` na raiz do repositório. O `.env` não é versionado.

| Variável | Valores | Padrão | Descrição |
| --- | --- | --- | --- |
| `DATABASE_URL` | URL do SQLAlchemy | `sqlite:///./tasks.db` | banco de dados; cria o arquivo `tasks.db` na raiz |
| `ENVIRONMENT` | `development`, `test`, `production` | `development` | em `production`, a documentação interativa (`/docs`, `/redoc`) e o `/openapi.json` ficam desabilitados; valor fora do conjunto impede a inicialização da aplicação |
| `LOCAL_UTC_OFFSET` | `±HH:MM` (por exemplo, `-03:00`, `+05:30`) | `-03:00` | fuso local das datas digitadas em `DD/MM/AAAA` e das datas devolvidas pela API (horário de Brasília). É um deslocamento fixo, sem horário de verão; valor fora do formato impede a inicialização da aplicação |

Exemplo de `.env`:

```dotenv
DATABASE_URL=sqlite:///./tasks.db
ENVIRONMENT=development
LOCAL_UTC_OFFSET=-03:00
```

As configurações são lidas uma única vez, na partida da aplicação: para mudar um valor, reinicie o servidor. As tabelas são criadas na partida, se ainda não existirem.

## Como rodar localmente

Pré-requisitos: Python 3.11 ou superior e Git.

### 1. Clonar o repositório

```bash
git clone https://github.com/luisZsiqueira/laboratorio-projeto.git
cd laboratorio-projeto
```

### 2. Criar e ativar o ambiente virtual

PowerShell (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Bash (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Git Bash (Windows): a ativação fica em `Scripts`, não em `bin`:

```bash
python3 -m venv .venv
source .venv/Scripts/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Rodar a API em desenvolvimento

```bash
python -m uvicorn app.main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`, e a documentação interativa em `http://127.0.0.1:8000/docs`. O log do *uvicorn* mostra `Application startup complete.` quando a aplicação está pronta; o primeiro início cria o arquivo `tasks.db` na raiz, que não é versionado. Para conferir, use o exemplo de [`GET /health`](#get-health-saúde-da-aplicação-e-do-banco).

### 5. Rodar os testes

```bash
python -m pytest -W error
```

Os testes usam SQLite em memória e não criam arquivos no repositório. Todos os comandos são executados a partir da raiz do repositório, com o `.venv` ativo. O projeto não usa checagem estática de tipos por ferramenta: o mypy foi retirado em 07/10/2026, porque o Smart App Control do Windows bloqueia as suas extensões compiladas (ADR-21 em [`docs/arquitetura.md`](docs/arquitetura.md)). Os *type hints* continuam obrigatórios e são conferidos na revisão de código.

### Solução de problemas (Windows)

Se `import sqlalchemy` falhar com `DLL load failed while importing _immutabledict_cy` e a mensagem "Uma política de Controle de Aplicativo bloqueou este arquivo", o Smart App Control do Windows está bloqueando as extensões compiladas do SQLAlchemy, que não são assinadas. Reinstale a mesma versão em Python puro, com o `.venv` ativo:

```powershell
$env:DISABLE_SQLALCHEMY_CEXT="1"
python -m pip install --force-reinstall --no-deps --no-binary SQLAlchemy SQLAlchemy==2.1.3
Remove-Item Env:DISABLE_SQLALCHEMY_CEXT
```

No Git Bash:

```bash
DISABLE_SQLALCHEMY_CEXT=1 python -m pip install --force-reinstall --no-deps --no-binary SQLAlchemy SQLAlchemy==2.1.3
```

A versão e o comportamento são os mesmos; só as otimizações em Cython ficam de fora.

## Roadmap de releases

Os itens de cada *release* (requisitos funcionais RF e técnicos RT), com critérios de aceite e estimativas, estão em [`docs/backlog.md`](docs/backlog.md).

| Release | Conteúdo | Situação |
| --- | --- | --- |
| `v0.1.0` | Fundação: estrutura, `.gitignore`, README, requisitos do curso, dependências verificadas, arquitetura e ADRs | concluída (04/10/2026, *tag* `v0.1.0`) |
| `v0.2.0` | Base técnica: configuração por ambiente, banco SQLite, aplicação FastAPI com `lifespan` e `/health` | concluída (05/10/2026, *tag* `v0.2.0`) |
| `v0.3.0` | CRUD de tarefas: criar, listar com filtro por *status*, consultar, atualizar (total e parcial), concluir e excluir | concluída (06/10/2026, *tag* `v0.3.0`) |
| `v0.4.0` | Prioridades e `priority_advisor` (coerência e sugestão, regras determinísticas), filtro por prioridade e datas no horário local | concluída (06/10/2026, *tag* `v0.4.0`) |
| `v0.5.0` | Revisão de arquitetura, de segurança, da documentação e das dependências; correções de segurança (`id` limitado, log sem os valores da requisição) e retirada do mypy | concluída (07/10/2026, *tag* `v0.5.0`) |
| `v1.0.0` | Entrega do curso: validação em máquina limpa, histórico de uso de IA consolidado com a análise final, *tag* e *Release* `v1.0.0` no GitHub | concluída (07/10/2026, *tag* e *Release* `v1.0.0`) |

## Uso de IA generativa

O projeto foi desenvolvido com apoio de IA generativa em todas as etapas do ciclo de vida: concepção, requisitos, planejamento, arquitetura, código, testes, revisão, documentação, validação e publicação.

| Assistente | Modelo | Etapas |
| --- | --- | --- |
| Claude (*chat*) | Claude Opus 5.5 | concepção do `CLAUDE.md` inicial a partir dos requisitos do curso, em 01 e 02/10/2026, antes do repositório |
| Claude Code | Claude Opus 5.5 | estrutura do projeto, `.gitignore`, README, verificação de versões e `requirements.txt`, desenho da arquitetura, licença, histórico de uso de IA, revisão de segredos e publicação no GitHub, revisão de publicação da `v0.1.0` (APIs deprecadas, ambiente virtual, *commits*, `CHANGELOG.md`), documento de escopo e requisitos do MVP, backlog por *release*, revisão dos diagramas Mermaid, regras de código e de *blueprint* executável |
| Claude in Chrome | Claude Opus 5.5 | conferência visual da renderização dos diagramas Mermaid no GitHub (Prompts 07, 12, 31 e 35) |
| Claude (*chat*) | Claude Sonnet 5.5 | extração, a partir de capturas de tela do curso, dos *prompts* de exemplo do tutor ([`docs/release-prompts-solon-020.md`](docs/release-prompts-solon-020.md)), em 04/10/2026 |
| Claude Code | Claude Fable 5.1 | planejamento dos *prompts* da fase de desenvolvimento ([`prompts/prompts-desenvolvimento.md`](prompts/prompts-desenvolvimento.md), Prompt 20) |
| Claude Code | Claude Sonnet 5.5 | execução do *blueprint* da `v0.2.0` ([`docs/blueprint-v020.md`](docs/blueprint-v020.md)): código da aplicação, testes de integração e execução manual da API (Prompts 22 e 23) |
| Claude Code | Claude Opus 5.5 | *blueprint* da `v0.2.0`, com protótipo verificado antes da aprovação (Prompt 21), e fechamento da *release*: revisão do README, ajuste dos diagramas, backlog, `CHANGELOG.md`, histórico de uso de IA e validação em clone limpo (Prompt 24) |
| Claude Code | Claude Opus 5.5 | *blueprint* da `v0.3.0` ([`docs/blueprint-v030.md`](docs/blueprint-v030.md)), com protótipo verificado e nova rodada do roteiro de APIs deprecadas (Prompt 25), e fechamento da *release* (Prompt 31) |
| Claude Code | Claude Sonnet 5.5 | execução do *blueprint* da `v0.3.0`: modelo, esquemas, *repository*, *service*, rotas, tradutores de erro e 56 testes novos (Prompts 26 a 29); exemplos de uso da seção Endpoints, executados na API (Prompt 30) |
| Claude Code | Claude Opus 5.5 | *blueprint* da `v0.4.0` ([`docs/blueprint-v040.md`](docs/blueprint-v040.md)), com protótipo verificado e a revisão das datas no horário local pedida pelo autor (Prompt 32), e fechamento da *release* (Prompt 35) |
| Claude Code | Claude Sonnet 5.5 | execução do *blueprint* da `v0.4.0`: `priority_advisor` e seus testes (Prompt 33); integração ao *service* e às rotas, filtro por prioridade, datas no horário local, 43 testes novos e exemplos do README executados na API (Prompt 34) |
| Claude Code | Claude Opus 5.5 | *blueprint* da `v0.5.0` ([`docs/blueprint-v050.md`](docs/blueprint-v050.md), Prompt 36); revisões de arquitetura (Prompt 37), de segurança, com duas correções, três testes novos e a retirada do mypy (Prompt 38), e da documentação e das dependências, com os exemplos do README executados de novo na API (Prompt 39); fechamento da *release* (Prompt 40) |
| Claude Code | Claude Opus 5.5 | *blueprint* da `v1.0.0` ([`docs/blueprint-v100.md`](docs/blueprint-v100.md), Prompt 41) e consolidação do histórico de uso de IA, com a análise final (Prompt 43); fechamento da entrega: checklist dos requisitos do curso, `CHANGELOG.md`, *tag* e *Release* `v1.0.0` e validação no clone da *tag* (Prompt 44) |
| Claude Code | Claude Sonnet 5.5 | validação em máquina limpa: clone, instalação, API, exemplos e testes só com os comandos do README, em PowerShell e em Git Bash (Prompt 42) |

- As regras de trabalho com o assistente estão em [`CLAUDE.md`](CLAUDE.md).
- Cada *prompt* usado fica registrado em [`prompts/`](prompts/), um arquivo por *prompt*; os *prompts* planejados para as *releases* `v0.2.0` a `v1.0.0` estão em [`prompts/prompts-desenvolvimento.md`](prompts/prompts-desenvolvimento.md).
- O histórico de uso da IA (etapas, ganhos, desafios, consolidação por *release* e análise final) está em [`docs/HISTORY-IA.md`](docs/HISTORY-IA.md); o uso anterior ao repositório, em [`docs/PRE-HISTORY-IA.md`](docs/PRE-HISTORY-IA.md); o uso em modo *chat* fora do repositório, em [`docs/EXTRA-HISTORY-IA.md`](docs/EXTRA-HISTORY-IA.md).
- Os *blueprints* aprovados ([`docs/blueprint-v020.md`](docs/blueprint-v020.md), [`docs/blueprint-v030.md`](docs/blueprint-v030.md), [`docs/blueprint-v040.md`](docs/blueprint-v040.md), [`docs/blueprint-v050.md`](docs/blueprint-v050.md) e [`docs/blueprint-v100.md`](docs/blueprint-v100.md)) são escritos para que um modelo de execução, como o Claude Sonnet 5.5, os siga sem depender do contexto da conversa (regra em [`CLAUDE.md`](CLAUDE.md), Blueprint executável).

Todo código gerado por IA é revisado e testado antes de ser incorporado.

## Limitações e próximos passos

Limitações conhecidas da versão atual:

- o fuso local é um deslocamento fixo (`LOCAL_UTC_OFFSET`), sem horário de verão; para uma região com horário de verão, o valor precisa ser trocado na mudança de horário;
- a API não registra se `due_at` foi informado só com o dia: a resposta mostra 23:59;
- a `suggested_priority` é calculada no momento de cada resposta e muda com o passar do tempo; ela não é gravada nem pode ser consultada em filtro;
- um `due_at` em formato não aceito responde `422` com uma entrada de erro para cada formato tentado (ISO com fuso e data local); a segunda traz no `loc` o nome do validador interno (`parse_local_due_at`), que não revela *stack trace*, SQL nem caminho e foi mantido para não mudar o formato do `422` (R-05 de [`docs/blueprint-v050.md`](docs/blueprint-v050.md));
- não há checagem estática de tipos por ferramenta: os *type hints* são conferidos na revisão de código (ADR-21);
- os comandos de Bash foram conferidos no Git Bash do Windows; a ativação para Linux/macOS (`source .venv/bin/activate`) não foi verificada em máquina Linux nem macOS.

Fora do escopo do MVP. São possibilidades futuras, não compromissos:

- autenticação e usuários;
- paginação na listagem;
- *frontend*;
- migrações de banco com Alembic;
- priorização assistida por IA (agente via API Claude).

O motivo de cada item ficar fora do MVP e os itens excluídos sem previsão estão em [`docs/escopo-mvp.md`](docs/escopo-mvp.md) (Fora de escopo).

## Créditos e licença

Desenvolvido por Luis Z Siqueira, com apoio do Claude Code, como miniprojeto do curso 1 da pós-graduação SWE-GENAI.

Distribuído sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE).
