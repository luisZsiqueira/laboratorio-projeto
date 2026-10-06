# Blueprint da `v0.4.0`: prioridades e `priority_advisor`

> **Status:** proposto em 06/10/2026 (Prompt 32) e revisado no mesmo dia, a pedido do autor, com a D-09 (datas no horário local, com só o dia valendo até 23:59). Aguarda aprovação do autor. Execução prevista: Prompt 33 (passo 1), Prompt 34 (passos 2 a 5) e Prompt 35 (passo 6, fechamento). Quem executa lê este arquivo e o `CLAUDE.md`; nada depende do histórico do *chat*.

## 1. Escopo da *release*

| ID | Item | Passo |
| --- | --- | --- |
| RT-10 | `app/services/priority_advisor.py` com funções puras e `tests/test_priority_advisor.py` | 1 |
| RF-09 | Prioridade e tipo da tarefa (aberta ou específica), com testes de integração | 3 |
| RF-10 | Validar coerência de prioridade (D-05) na criação, no `PUT` e no `PATCH` | 1, 2 e 3 |
| RF-11 | Sugerir prioridade pela proximidade do prazo (D-07), na resposta | 1, 2 e 3 |
| RF-14 | Filtrar a listagem por prioridade (D-06, aprovado neste *blueprint*) | 2 e 3 |
| RF-09 (ampliado pela D-09) | `due_at` digitado no horário local (`DD/MM/AAAA HH:MM` ou só `DD/MM/AAAA`, valendo até 23:59) e datas devolvidas no fuso local configurado (`LOCAL_UTC_OFFSET`) | 4 |
| RT-09 (critério 3, ampliado) | Exemplos de uso do README com prioridade, sugestão, filtro e datas no horário local | 5 |

Critérios de aceite: os de `docs/backlog.md` (seção 4.3), os de RF-14 e da D-09 na seção 2.1 abaixo e os critérios comuns do backlog (seção 2). Fluxos: `docs/arquitetura.md`, seção 3. ADRs aplicados: ADR-01, ADR-06, ADR-10, ADR-12, ADR-14, ADR-15, e os novos ADR-16, ADR-17 e ADR-18 (este ajusta o ADR-10 e o ADR-15).

## 2. Decisões tomadas

Não há decisão em aberto neste *blueprint*. As decisões abaixo são confirmadas na aprovação.

### 2.1 Decisões de escopo (D-05 a D-07 e D-09)

D-05 a D-07 seguem a recomendação de `docs/escopo-mvp.md`, seção 6, com o detalhamento abaixo. A D-09 é nova, pedida pelo autor na revisão deste *blueprint* (06/10/2026), e muda o escopo do RF-09 e do RNF-11. Todas são migradas para os requisitos ou ADRs no fechamento (passo 6).

| ID | Decisão |
| --- | --- |
| D-05 | Prioridade 4 (agendada) exige `due_at`. `due_at` não exige prioridade 4: uma tarefa de prioridade 1 a 3 pode ter prazo. A regra vale na criação, no `PUT` e no `PATCH`. No `PATCH`, ela é conferida no **estado resultante** (campos enviados sobre os gravados): `{"priority": 4}` numa tarefa sem prazo e `{"due_at": null}` numa tarefa de prioridade 4 são incoerentes. Violação: exceção de domínio `IncoherentPriorityError`, traduzida em `422` com `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`. A conclusão (`POST /tasks/{id}/complete`) e a exclusão não conferem a regra |
| D-06 | **Incluir** o filtro por prioridade como RF-14: `GET /tasks?priority=<1 a 4>`, nos moldes do RF-03; combinado com `?status=`, os dois filtros se somam (E lógico); valor fora de 1 a 4 ou não inteiro responde `422`. Motivo, pelas horas reais do `docs/backlog.md`: até a `v0.3.0` foram 12 h. Com a `v0.4.0` (7,25 h, seção 10), a `v0.5.0` (2,5 h + 1,5 h de *blueprint* e fechamento) e a `v1.0.0` (2 h + 1 h), a projeção é de cerca de 26,3 h. Ficam cerca de 3,7 h de folga no orçamento de cerca de 30 h para o tempo não medido da `v0.1.0` e para imprevistos. O RF-14 custa 0,5 h e reaproveita o padrão do RF-03 |
| D-07 | Validação de coerência (D-05) na criação e na atualização. Sugestão pela proximidade do prazo devolvida como campo calculado `suggested_priority` em todas as respostas de tarefa (`TaskRead`), **sem alterar nem gravar** a prioridade. A sugestão é calculada a cada resposta, com o instante atual como referência, pelas regras da tabela da seção 2.2. Não há coluna nova: o esquema do banco é o mesmo da `v0.3.0` |
| D-09 | Datas no horário local, para preenchimento por pessoas. **Entrada** de `due_at` (`POST`, `PUT`, `PATCH`), em três formatos: `DD/MM/AAAA HH:MM` (horário local); `DD/MM/AAAA` (horário local, valendo até **23:59** do dia); ISO 8601 **com** fuso (como na `v0.3.0`, para programas). Qualquer outro formato responde `422`, inclusive ISO só com a data (`2026-10-20`), ISO sem fuso, data inexistente (`31/02/2026`), ano com dois dígitos e hora sem os minutos. **Fuso local:** deslocamento fixo `±HH:MM` lido da nova variável de ambiente `LOCAL_UTC_OFFSET`, padrão `-03:00` (horário de Brasília, sem horário de verão). **Saída:** `due_at`, `created_at` e `updated_at` devolvidos em ISO 8601 no fuso local (`2026-10-20T23:59:00-03:00`), e não mais em UTC com `Z`. **Persistência:** sem mudança, em UTC (DT-04). Não fica registrado se o usuário informou só o dia: a resposta mostra 23:59 |

Critérios de aceite do RF-14, a registrar no `docs/backlog.md` e no `docs/escopo-mvp.md` no fechamento: (1) `?priority=` devolve só as tarefas com aquela prioridade **[T]**; (2) combinado com `?status=`, devolve as que atendem aos dois **[T]**; (3) valor fora de 1 a 4 ou não inteiro responde **422** **[T]**.

Critérios de aceite da D-09, que substituem o critério 3 do RF-09 no fechamento: (1) `DD/MM/AAAA HH:MM` gravado como horário local **[T]**; (2) `DD/MM/AAAA` gravado como 23:59 local, no `POST` e no `PATCH` **[T]**; (3) formatos fora dos três aceitos respondem **422** **[T]**; (4) as datas da resposta vêm no deslocamento de `LOCAL_UTC_OFFSET` **[T]**; (5) `LOCAL_UTC_OFFSET` fora de `±HH:MM` impede a partida **[T]**.

### 2.2 Regras de sugestão (RF-11)

`remaining = due_at - reference_time`, com as duas datas *timezone-aware*. Os limites pertencem à faixa de menor prioridade numérica (mais urgente).

| Situação | Tempo restante (`remaining`) | `suggested_priority` |
| --- | --- | --- |
| tarefa concluída (`status == "done"`) | qualquer | `null` |
| tarefa aberta (`due_at` nulo) | — | `null` |
| prazo vencido ou próximo | `remaining <= 4 h` (inclui negativo e zero) | `1` (mandatória) |
| prazo no dia | `4 h < remaining <= 24 h` | `2` (importante) |
| prazo na semana | `24 h < remaining <= 7 dias` | `3` (regular) |
| prazo distante | `remaining > 7 dias` | `4` (agendada) |

A sugestão `4` só ocorre com `due_at` preenchido, portanto é sempre coerente com a D-05. As faixas são regra de negócio, não configuração: ficam como constantes `timedelta` no `priority_advisor` (DT-09), sem variável de ambiente.

### 2.3 Novos ADRs

Registrados em `docs/arquitetura.md`, seção 6, no passo indicado.

| ID | Decisão | Motivo | Passo |
| --- | --- | --- | --- |
| ADR-16 | `app/services/priority_advisor.py` contém só funções puras e a exceção `IncoherentPriorityError`; importa apenas `datetime` e os tipos de `task_schemas.py`. Não importa banco, *repository*, FastAPI nem Starlette e não lê o relógio: a data/hora de referência é parâmetro. O instante atual vem do relógio injetado no *service*: `TaskService(repository: TaskStore, clock: Callable[[], datetime] = utc_now)`. Quem chama o *advisor* é só o `task_service` | regras determinísticas e testáveis sem banco, sem HTTP e sem depender do instante da execução (RNF-03); o *service* continua o único ponto de regra de negócio (ADR-01) | 2 |
| ADR-17 | Contrato da `v0.4.0`, somado ao ADR-15: `TaskRead` ganha `suggested_priority` (`TaskPriority` ou `null`), calculado a cada resposta e nunca gravado (D-07); combinação incoerente (D-05) responde `422` com `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`, no formato dos outros erros de domínio (`404`, `500`) e não no formato de lista da validação do FastAPI; `GET /tasks` aceita `?priority=` (1 a 4), combinável com `?status=` (RF-14) | mensagem única e clara para a regra de negócio; o cliente distingue erro de forma (lista) de erro de regra (texto); a prioridade gravada continua sendo a escolha do usuário | 3 |
| ADR-18 | Horário local na fronteira da API (D-09), ajustando o ADR-10 e o ADR-15: o banco continua em UTC; a entrada aceita `DD/MM/AAAA HH:MM` e `DD/MM/AAAA` (23:59) no fuso local, além de ISO 8601 com fuso; as respostas trazem as datas no fuso local. O fuso é o deslocamento fixo de `LOCAL_UTC_OFFSET` (`Settings`), passado ao *service* (`TaskService(..., local_timezone=...)`), que acrescenta o fuso às datas locais da entrada e converte as datas da resposta em `build_task_read`. A rota obtém as `Settings` da aplicação em `request.app.state.settings`, gravadas por `create_app` | formato fácil de digitar e de ler; a conversão fica num único ponto (o *service*), sem regra nos esquemas além do reconhecimento do formato; a persistência em UTC (DT-04) não muda, e o ISO com fuso continua aceito para quem já usa a API | 4 |

### 2.4 Decisões técnicas (DT)

Registradas em `docs/decisoes.md` no mesmo passo do código que as aplica.

| ID | Decisão | Passo |
| --- | --- | --- |
| DT-09 | Faixas da sugestão como constantes `timedelta` no `priority_advisor` (`MANDATORY_WINDOW = timedelta(hours=4)`, `IMPORTANT_WINDOW = timedelta(hours=24)`, `REGULAR_WINDOW = timedelta(days=7)`), com limites inclusivos na faixa mais urgente. `suggest_priority` levanta `ValueError` se `reference_time` ou `due_at` não tiver fuso. Alternativas descartadas: variáveis de ambiente, porque são regra de negócio e não configuração de implantação; limites exclusivos, porque deixariam um prazo de exatamente 4 h fora da faixa mandatória | 1 |
| DT-10 | No `PATCH`, a coerência é conferida no estado resultante **antes** de alterar a tarefa: `priority` vem do corpo se não for `None` (o `PATCH` já recusa `null` nesse campo, DT-05), senão da tarefa; `due_at` vem do corpo se `"due_at" in task_data.model_fields_set` (inclui `null` explícito), senão da tarefa. Alternativa descartada: aplicar as mudanças e validar depois, porque deixaria o objeto ORM alterado na sessão em caso de erro e confundiria o dublê dos testes unitários | 2 |
| DT-11 | A resposta é montada no *service* por `build_task_read(task) -> TaskRead`, que faz `TaskRead.model_validate(task).model_copy(update={"suggested_priority": ...})`; em `TaskRead`, `suggested_priority` tem padrão `None` para que o `model_validate` a partir do ORM funcione. As rotas trocam `TaskRead.model_validate(...)` por `service.build_task_read(...)`. Alternativas descartadas: `@computed_field` no esquema, porque daria lógica aos modelos e faria `app/models/` importar `app/services/`; calcular na rota, porque poria regra de negócio no *controller*; os casos de uso devolverem `TaskRead`, porque mudaria os 14 testes unitários da `v0.3.0`, que conferem o objeto `Task` | 2 |
| DT-12 | `TaskPriorityQuery = Annotated[TaskPriority, BeforeValidator(convert_priority_text)]` em `task_schemas.py` para o parâmetro de consulta `priority`. Motivo verificado no protótipo: o `Literal[1, 2, 3, 4]` não converte o texto `"1"` da *query string* e responde `422` para `?priority=1`. `convert_priority_text` converte só texto com dígitos decimais (`str.isdecimal()`); o resto segue para o `Literal`, que recusa com a mensagem padrão (`Input should be 1, 2, 3 or 4`). Alternativas descartadas: `int` com `Query(ge=1, le=4)`, porque o `CLAUDE.md` exige `Literal` para conjuntos fechados; `BeforeValidator(int)`, porque a mensagem de `?priority=alta` exporia o texto interno do `int()` (`invalid literal for int() with base 10`) | 3 |
| DT-13 | `due_at` nos três esquemas de entrada passa a ser `TaskDueAt \| None`, com `TaskDueAt = AwareDatetime \| LocalDueAt` e `LocalDueAt = Annotated[NaiveDatetime, BeforeValidator(parse_local_due_at)]`. `parse_local_due_at` tenta `datetime.strptime` com `"%d/%m/%Y %H:%M"` e, em seguida, com `"%d/%m/%Y"` combinado com `END_OF_DAY = time(23, 59)`; texto em outro formato levanta `ValueError` com a mensagem "use DD/MM/AAAA HH:MM, DD/MM/AAAA ou ISO 8601 com fuso horário". Na união, o ISO com fuso é aceito pelo primeiro ramo; o ISO sem fuso falha nos dois (`422`). Alternativas descartadas: aceitar ISO só com a data, porque o Pydantic o converte para 00:00 (o oposto de "até o fim do dia"); 23:59:59, porque 23:59 é mais legível e não muda a sugestão | 4 |
| DT-14 | `LOCAL_UTC_OFFSET` é texto validado por padrão (`UtcOffset = Annotated[str, StringConstraints(pattern=r"^[+-](0\d\|1[0-4]):[0-5]\d$")]`) e convertido em `datetime.timezone` por `parse_utc_offset` no *service*. Alternativas descartadas: `ZoneInfo("America/Sao_Paulo")`, porque falha nesta máquina com `ZoneInfoNotFoundError` (o Windows não traz a base IANA e o pacote `tzdata` não está no `requirements.txt`); campo `timedelta`, porque o Pydantic aceita `-3` como 3 segundos negativos. Consequência: o deslocamento é fixo e não acompanha horário de verão (limitação registrada no README) | 4 |
| DT-15 | `create_app` grava as `Settings` em `application.state.settings`, e `get_task_service` as lê de `request.app.state.settings` (anotada como `Settings`) para compor o *service*. Alternativa descartada: `Depends(get_settings)` na rota, porque leria o ambiente e o `.env` da máquina, e não as `Settings` passadas a `create_app` nos testes (DT-01, DT-02) | 4 |

## 3. Verificação prévia

O código deste *blueprint* foi executado em protótipo fora do repositório (diretório temporário do assistente), em 06/10/2026, no `.venv` do projeto (Python 3.14.6 e as versões do `requirements.txt`):

- `python -m pytest -W error`: 91 testes ao fim do passo 1, 100 ao fim do passo 2, 114 ao fim do passo 3 e 134 ao fim do passo 4 (69 da `v0.3.0` e 65 novos: 22 do *advisor*, 14 do *service* e 29 das rotas);
- `python -m mypy --explicit-package-bases app`: sem erros em 18 arquivos;
- `GET /openapi.json`: `suggested_priority` documentado como inteiro de 1 a 4 ou `null`; o parâmetro `priority` aparece como `enum [1, 2, 3, 4]`;
- `POST /tasks` com `{"title": "Consulta", "priority": 4, "due_at": "20/10/2026"}`: `201` com `due_at` igual a `"2026-10-20T23:59:00-03:00"`, datas de controle em `-03:00` e `suggested_priority` `4`.

O protótipo revelou seis pontos já incorporados aqui:

- o `Literal` de inteiros recusa `?priority=1` na *query string* (DT-12);
- `status.HTTP_422_UNPROCESSABLE_CONTENT` existe no Starlette 1.7.0 e não emite aviso com `-W error`; ela substitui no código a constante proibida `HTTP_422_UNPROCESSABLE_ENTITY` (seção 5.2);
- o dublê `InMemoryTaskRepository` precisa aceitar o novo parâmetro `priority` de `find_all`, senão dois testes da `v0.3.0` falham com `TypeError`;
- `ZoneInfo("America/Sao_Paulo")` falha nesta máquina sem o pacote `tzdata` (DT-14);
- o Pydantic aceita ISO só com a data e o converte para 00:00, e aceita `-3` como `timedelta` de 3 segundos (DT-13 e DT-14);
- o teste `test_create_task_rejects_invalid_body_with_422` da `v0.3.0` usa `"10/10/2026"` como data inválida; com a D-09 esse texto é válido e o caso passa a usar `"10-10-2026"` (passo 4).

## 4. Contrato da API

Somente as mudanças em relação ao ADR-15 (`docs/blueprint-v030.md`, seção 4):

| Método e caminho | Mudança | Sucesso | Erros novos |
| --- | --- | --- | --- |
| `POST /tasks` | confere D-05 | `201` com `TaskRead` (com `suggested_priority`) | `422` incoerente |
| `GET /tasks?status=&priority=` | novo filtro `priority` (RF-14) | `200` com `list[TaskRead]` | `422` (`priority` fora de 1 a 4 ou não inteiro) |
| `GET /tasks/{task_id}` | — | `200` com `TaskRead` (com `suggested_priority`) | — |
| `PUT /tasks/{task_id}` | confere D-05 no corpo | `200` com `TaskRead` | `422` incoerente |
| `PATCH /tasks/{task_id}` | confere D-05 no estado resultante | `200` com `TaskRead` | `422` incoerente |
| `POST /tasks/{task_id}/complete` | — | `200` com `TaskRead` (`suggested_priority` nulo, pois `done`) | — |
| `DELETE /tasks/{task_id}` | — | `204` | — |

Ordem das verificações em `PUT` e `PATCH`: primeiro o corpo (validação Pydantic, `422` em lista), depois a existência da tarefa (`404`), depois a coerência (`422` com texto). Assim, `PUT /tasks/99` com prioridade 4 sem prazo responde `404`.

Exemplo de `422` incoerente:

```json
{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}
```

Datas (D-09, ADR-18), em todos os endpoints de tarefa:

| `due_at` enviado | Gravado (UTC) | Devolvido (com `LOCAL_UTC_OFFSET=-03:00`) |
| --- | --- | --- |
| `"20/10/2026 14:30"` | 20/10/2026 17:30 | `"2026-10-20T14:30:00-03:00"` |
| `"20/10/2026"` | 21/10/2026 02:59 | `"2026-10-20T23:59:00-03:00"` |
| `"2026-10-20T17:30:00Z"` | 20/10/2026 17:30 | `"2026-10-20T14:30:00-03:00"` |
| `"2026-10-20"`, `"2026-10-20T14:30:00"`, `"31/02/2026"`, `"20/10/26"`, `"20/10/2026 14h"`, `"10-10-2026"` | — | `422` (lista de erros da validação) |

`created_at` e `updated_at` também são devolvidos no fuso local.

## 5. APIs: permitidas e proibidas

### 5.1 Importações permitidas

Usar exatamente estas linhas, por arquivo (estado final de cada arquivo). Nenhuma outra importação de terceiros. Os arquivos não listados aqui não mudam.

```python
# app/services/priority_advisor.py (novo)
from datetime import datetime, timedelta
from app.models.task_schemas import TaskPriority, TaskStatus

# app/models/settings.py
from functools import lru_cache
from typing import Annotated, Literal
from pydantic import StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict

# app/models/task_schemas.py
from datetime import datetime, time
from typing import Annotated, Literal
from pydantic import AwareDatetime, BaseModel, BeforeValidator, ConfigDict, NaiveDatetime, StringConstraints, field_validator

# app/repositories/task_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.task_schemas import TaskPriority, TaskStatus

# app/services/task_service.py
from collections.abc import Callable, Mapping
from datetime import UTC, datetime, timedelta, timezone
from typing import Protocol
from sqlalchemy.orm import Session
from app.models.base import utc_now
from app.models.task import Task
from app.models.task_schemas import TaskCreate, TaskPatch, TaskPriority, TaskRead, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import ensure_priority_is_coherent, suggest_priority

# app/api/error_handlers.py
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.services.priority_advisor import IncoherentPriorityError
from app.services.task_service import TaskNotFoundError

# app/api/task_routes.py
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from app.models.settings import Settings
from app.models.task_schemas import TaskCreate, TaskPatch, TaskPriorityQuery, TaskRead, TaskStatus, TaskUpdate
from app.repositories.database import get_db
from app.services.task_service import TaskService, build_task_service

# tests/test_priority_advisor.py (novo)
from datetime import UTC, datetime, timedelta, timezone
import pytest
from app.models.task_schemas import TaskPriority
from app.services.priority_advisor import IncoherentPriorityError, ensure_priority_is_coherent, suggest_priority

# tests/test_task_service.py
from datetime import UTC, datetime, timedelta, timezone
import pytest
from app.models.task import Task
from app.models.task_schemas import TaskCreate, TaskPatch, TaskPriority, TaskStatus, TaskUpdate
from app.services.priority_advisor import IncoherentPriorityError
from app.services.task_service import TaskNotFoundError, TaskService, parse_utc_offset
```

`app/main.py` não ganha importações (só a linha `application.state.settings = settings`, no passo 4). `tests/test_task_routes.py` não ganha importações: os testes novos usam `datetime`, `UTC`, `timedelta`, `pytest`, `ValidationError`, `Engine` e `Settings`, já importados. Em `tests/test_task_service.py`, o passo 2 acrescenta `datetime`, `timedelta` e `IncoherentPriorityError`, e o passo 4 acrescenta `timezone` e `parse_utc_offset`. As linhas longas acima são escritas no arquivo com parênteses e uma importação por linha, no estilo dos arquivos existentes.

### 5.2 Padrões proibidos

Do roteiro de checagem do `CLAUDE.md` e da rodada desta *release* (verificados em 06/10/2026 nas versões fixadas, com `python -W error`):

| Proibido | Usar | Situação verificada |
| --- | --- | --- |
| `status.HTTP_422_UNPROCESSABLE_ENTITY` | `status.HTTP_422_UNPROCESSABLE_CONTENT` no código; o inteiro `422` nos testes | constante antiga: `StarletteDeprecationWarning` (já no roteiro); a nova: sem aviso (Starlette 1.7.0): **novo**, atualizar a linha do roteiro no passo 3 |
| `Literal[1, 2, 3, 4]` puro em parâmetro de consulta | `TaskPriorityQuery` (DT-12) | `?priority=1` responde `422` (FastAPI 0.142.2, Pydantic 2.13.5) |
| `datetime.now()` ou `utc_now()` dentro do `priority_advisor` | `reference_time` recebido como parâmetro (ADR-16) | regra deste *blueprint* |
| `@computed_field` em `TaskRead` | `TaskService.build_task_read` (DT-11) | regra deste *blueprint* |
| `zoneinfo.ZoneInfo` e o pacote `tzdata` | deslocamento fixo `LOCAL_UTC_OFFSET` e `parse_utc_offset` (DT-14) | `ZoneInfoNotFoundError` no Windows sem `tzdata` (Python 3.14.6) |
| `timedelta` como tipo de `LOCAL_UTC_OFFSET` | `UtcOffset` (texto com padrão, DT-14) | o Pydantic aceita `-3` como 3 segundos (Pydantic 2.13.5) |
| `AwareDatetime` sozinho em `due_at` na entrada; ISO só com a data | `TaskDueAt` (DT-13) | ISO só com a data vira 00:00 (Pydantic 2.13.5) |
| `"-03:00"` ou outro deslocamento escrito fora de `settings.py` | `Settings.local_utc_offset`; nos testes, o argumento `local_utc_offset` de `open_test_client` | literal de configuração (`CLAUDE.md`) |
| `datetime.utcnow()` | `utc_now()` de `app/models/base.py` ou `datetime.now(UTC)` nos testes | já no roteiro |
| `.dict()`, `.from_orm()`, `@validator`, `class Config:` | `model_dump()`, `model_validate()`, `@field_validator`/`BeforeValidator`, `ConfigDict` | já no roteiro |
| `session.query(...)` | `select(...)` com `session.scalars` | já no roteiro (estilo legado) |
| `Optional[X]` | `X \| None` | convenção do `CLAUDE.md` |

Também proibidos nesta *release*: coluna nova ou alteração da tabela `tasks`; gravar `suggested_priority`; gravar datas fora de UTC; SQL textual ou montado por concatenação; `Any` e `# type: ignore` em `app/`; `type X = ...` (Python 3.12); `__init__.py` em `app/` ou em `tests/`; acesso ao banco nas rotas; importação de FastAPI ou Starlette no *service* ou no *advisor*; `unittest.mock`; IA, rede ou serviço externo no *advisor*.

## 6. Passos

Cada passo termina com a definição de pronto verde, na raiz do repositório, com o `.venv` ativo:

```bash
python -m pytest -W error
python -m mypy --explicit-package-bases app
```

Todas as classes e funções públicas recebem *docstring* em português no formato da `v0.3.0` (propósito; `Args`, `Returns` e `Raises` quando houver). Os testes novos são acrescentados ao **final** de cada arquivo de teste existente; os testes da `v0.3.0` não mudam, salvo o dublê indicado no passo 2.

### Passo 1: `priority_advisor` e testes unitários (RT-10, RF-10, RF-11) — Prompt 33

**Arquivos a criar:** `app/services/priority_advisor.py`, `tests/test_priority_advisor.py`. **A alterar:** `docs/decisoes.md` (DT-09).

**`app/services/priority_advisor.py`.** Código completo (as *docstrings* abaixo são as do arquivo):

```python
MANDATORY_WINDOW = timedelta(hours=4)
IMPORTANT_WINDOW = timedelta(hours=24)
REGULAR_WINDOW = timedelta(days=7)


class IncoherentPriorityError(Exception):
    """Sinaliza combinação incoerente de prioridade e prazo (D-05).

    Attributes:
        priority: prioridade recusada.
    """

    def __init__(self, priority: TaskPriority) -> None:
        """Monta a mensagem e guarda a prioridade recusada.

        Args:
            priority: prioridade que exige um prazo ausente.
        """
        super().__init__(f"prioridade {priority} (agendada) exige due_at preenchido")
        self.priority = priority


def ensure_priority_is_coherent(priority: TaskPriority, due_at: datetime | None) -> None:
    """Confere a coerência entre prioridade e prazo (D-05).

    Regra: prioridade 4 (agendada) exige `due_at`; `due_at` não exige prioridade 4.

    Args:
        priority: prioridade da tarefa.
        due_at: prazo da tarefa, ou `None` (tarefa aberta).

    Raises:
        IncoherentPriorityError: se `priority` for 4 e `due_at` for `None`.
    """
    if priority == 4 and due_at is None:
        raise IncoherentPriorityError(priority)


def suggest_priority(
    status: TaskStatus, due_at: datetime | None, reference_time: datetime
) -> TaskPriority | None:
    """Sugere a prioridade pela proximidade do prazo (D-07, DT-09).

    Sem sugestão (`None`) para tarefa concluída ou aberta. Com prazo, pelo tempo
    restante `due_at - reference_time`: até 4 h (inclusive vencido), 1; até 24 h,
    2; até 7 dias, 3; acima de 7 dias, 4. Os limites pertencem à faixa menor.

    Args:
        status: situação da tarefa.
        due_at: prazo da tarefa, com fuso horário, ou `None`.
        reference_time: instante de referência, com fuso horário.

    Returns:
        A prioridade sugerida, ou `None` se não houver base para sugerir.

    Raises:
        ValueError: se `reference_time` ou `due_at` não tiver fuso horário.
    """
    if reference_time.tzinfo is None:
        raise ValueError("a data/hora de referência precisa de fuso horário")
    if status == "done" or due_at is None:
        return None
    if due_at.tzinfo is None:
        raise ValueError("o prazo precisa de fuso horário")
    remaining = due_at - reference_time
    if remaining <= MANDATORY_WINDOW:
        return 1
    if remaining <= IMPORTANT_WINDOW:
        return 2
    if remaining <= REGULAR_WINDOW:
        return 3
    return 4
```

**`tests/test_priority_advisor.py`.** Constante `REFERENCE_TIME = datetime(2026, 10, 10, 12, 0, tzinfo=UTC)` no topo; sem *fixture*.

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_priority_four_without_due_at_is_incoherent` | `ensure_priority_is_coherent(4, None)` | levanta `IncoherentPriorityError`; `error.priority == 4`; `str(error) == "prioridade 4 (agendada) exige due_at preenchido"` |
| `test_priority_four_with_due_at_is_coherent` | `ensure_priority_is_coherent(4, REFERENCE_TIME)` | não levanta |
| `test_priorities_one_to_three_are_coherent_with_or_without_due_at` | dois `@pytest.mark.parametrize`: `priority` em `[1, 2, 3]` e `due_at` em `[None, REFERENCE_TIME]` (6 casos); parâmetro `priority: TaskPriority` | não levanta |
| `test_suggest_priority_returns_none_for_open_task` | `suggest_priority("pending", None, REFERENCE_TIME)` | `None` |
| `test_suggest_priority_returns_none_for_done_task` | `suggest_priority("done", REFERENCE_TIME + timedelta(hours=1), REFERENCE_TIME)` | `None` |
| `test_suggest_priority_by_deadline_proximity` | `parametrize(("remaining", "expected_priority"), ...)` com 9 casos: `(timedelta(days=-1), 1)`, `(timedelta(0), 1)`, `(timedelta(hours=4), 1)`, `(timedelta(hours=4, seconds=1), 2)`, `(timedelta(hours=24), 2)`, `(timedelta(hours=24, seconds=1), 3)`, `(timedelta(days=7), 3)`, `(timedelta(days=7, seconds=1), 4)`, `(timedelta(days=30), 4)`; `due_at = REFERENCE_TIME + remaining`, `status = "pending"` | `== expected_priority` |
| `test_suggest_priority_accepts_due_at_in_other_timezone` | `due_at = datetime(2026, 10, 10, 14, 0, tzinfo=timezone(timedelta(hours=-3)))` (17:00 UTC, 5 h depois da referência) | `2` (se o fuso fosse ignorado, seriam 2 h e o resultado `1`) |
| `test_suggest_priority_rejects_naive_datetimes` | `parametrize(("due_at", "reference_time"), ...)` com `(REFERENCE_TIME, datetime(2026, 10, 10, 12, 0))` e `(datetime(2026, 10, 11, 12, 0), REFERENCE_TIME)` | levanta `ValueError` |

**Verificação:** definição de pronto; 91 testes passando (69 + 22); mypy sem erros em 18 arquivos.

**IDs:** RT-10 (critérios 1 a 3), RF-10 e RF-11 (regras), D-05, D-07, ADR-16 (contrato do *advisor*), DT-09.

### Passo 2: esquema de leitura, *repository* e *service* (RF-10, RF-11, RF-14) — Prompt 34

**Arquivos a alterar:** `app/models/task_schemas.py`, `app/repositories/task_repository.py`, `app/services/task_service.py`, `tests/test_task_service.py`, `docs/decisoes.md` (DT-10 e DT-11), `docs/arquitetura.md` (ADR-16 na tabela da seção 6).

**`app/models/task_schemas.py`:** em `TaskRead`, acrescentar ao final o campo `suggested_priority: TaskPriority | None = None` e, na *docstring*, o atributo `suggested_priority: prioridade sugerida pela proximidade do prazo, calculada na resposta e nunca gravada (D-07); None para tarefa aberta ou concluída.` Nada mais muda neste passo.

**`app/repositories/task_repository.py`:** `find_all(self, status: TaskStatus | None, priority: TaskPriority | None = None) -> list[Task]`; depois do filtro de `status`, `if priority is not None: statement = statement.where(Task.priority == priority)`. *Docstring* com o novo argumento.

**`app/services/task_service.py`:**

- `TaskStore.find_all(self, status: TaskStatus | None, priority: TaskPriority | None = None) -> list[Task]` (*docstring*: "Devolve as tarefas por `id`, filtradas por situação e prioridade.").
- `TaskService.__init__(self, repository: TaskStore, clock: Callable[[], datetime] = utc_now) -> None`: guarda `self.repository` e `self.clock` (ADR-16). *Docstring* da classe: "Recebe o *repository* e o relógio por injeção (ADR-14, ADR-16)."
- `create_task`: primeira linha `ensure_priority_is_coherent(task_data.priority, task_data.due_at)`; o resto não muda (`created_at` continua vindo de `utc_now()`). `Raises: IncoherentPriorityError`.
- `list_tasks(self, status: TaskStatus | None, priority: TaskPriority | None = None) -> list[Task]`: devolve `self.repository.find_all(status, priority)`.
- `replace_task`: depois de `get_task`, `ensure_priority_is_coherent(task_data.priority, task_data.due_at)` e só então `apply_changes`. `Raises: IncoherentPriorityError`.
- `patch_task` (DT-10), depois de `get_task` e antes de `apply_changes`:

```python
        task = self.get_task(task_id)
        resulting_priority = (
            task_data.priority if task_data.priority is not None else task.priority
        )
        resulting_due_at = (
            task_data.due_at if "due_at" in task_data.model_fields_set else task.due_at
        )
        ensure_priority_is_coherent(resulting_priority, resulting_due_at)
        apply_changes(task, task_data.model_dump(exclude_unset=True))
        return self.repository.save(task)
```

- `complete_task` e `delete_task` não mudam.
- Novo método, depois de `delete_task` (DT-11):

```python
    def build_task_read(self, task: Task) -> TaskRead:
        """Monta a resposta da tarefa com a prioridade sugerida (D-07, DT-11).

        A sugestão usa o instante do relógio do *service* e não altera a tarefa
        nem a prioridade gravada.

        Args:
            task: tarefa carregada.

        Returns:
            O `TaskRead` com `suggested_priority` preenchido.
        """
        suggestion = suggest_priority(task.status, task.due_at, self.clock())
        return TaskRead.model_validate(task).model_copy(
            update={"suggested_priority": suggestion}
        )
```

**`tests/test_task_service.py`.** Acrescentar `REFERENCE_TIME = datetime(2026, 10, 10, 12, 0, tzinfo=UTC)` depois das importações. Alterar só a assinatura e o filtro de `InMemoryTaskRepository.find_all`:

```python
    def find_all(
        self, status: TaskStatus | None, priority: TaskPriority | None = None
    ) -> list[Task]:
        """Devolve as tarefas por id, filtradas por status e prioridade se informados."""
        return [
            task
            for task_id, task in sorted(self.tasks.items())
            if (status is None or task.status == status)
            and (priority is None or task.priority == priority)
        ]
```

Acrescentar, depois da *fixture* `service`:

```python
@pytest.fixture
def clocked_service(repository: InMemoryTaskRepository) -> TaskService:
    """Service com relógio fixo em REFERENCE_TIME, para sugestões determinísticas."""
    return TaskService(repository, clock=lambda: REFERENCE_TIME)
```

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_create_task_rejects_priority_four_without_due_at` | `service.create_task(TaskCreate(title="A", priority=4))` | levanta `IncoherentPriorityError`; `repository.tasks == {}` |
| `test_create_task_accepts_priority_four_with_due_at` | `TaskCreate(title="A", priority=4, due_at=REFERENCE_TIME)` | `(task.priority, task.due_at) == (4, REFERENCE_TIME)` |
| `test_replace_task_rejects_incoherent_priority_without_saving` | `create_sample_task`; `replace_task(id, TaskUpdate(title="B", description=None, status="pending", priority=4, due_at=None))` | levanta `IncoherentPriorityError`; `(task.title, task.priority) == ("Estudar FastAPI", 3)`; `repository.save_count == 0` |
| `test_patch_task_rejects_priority_four_when_task_has_no_due_at` | `create_sample_task`; `patch_task(id, TaskPatch(priority=4))` | levanta; `task.priority == 3`; `save_count == 0` |
| `test_patch_task_rejects_clearing_due_at_of_priority_four_task` | criar `TaskCreate(title="A", priority=4, due_at=REFERENCE_TIME)`; `patch_task(id, TaskPatch(due_at=None))` | levanta; `task.due_at == REFERENCE_TIME`; `save_count == 0` |
| `test_patch_task_accepts_priority_four_with_due_at_sent_together` | `create_sample_task`; `patch_task(id, TaskPatch(priority=4, due_at=REFERENCE_TIME))` | `(priority, due_at) == (4, REFERENCE_TIME)` |
| `test_build_task_read_includes_suggestion_without_changing_priority` | `clocked_service.create_task(TaskCreate(title="A", due_at=REFERENCE_TIME + timedelta(hours=2)))`; `build_task_read(task)` | `suggested_priority == 1`; `task_read.priority == 3`; `task.priority == 3` |
| `test_build_task_read_has_no_suggestion_for_open_task` | `create_sample_task(clocked_service)`; `build_task_read(task)` | `suggested_priority is None` |
| `test_list_tasks_filters_by_priority` | criar `("A", 1)`, `("B", 2)`, `("C", 1)` como `TaskCreate(title=..., priority=...)`; `service.list_tasks(None, 1)` | títulos `["A", "C"]` |

**Verificação:** definição de pronto; 100 testes passando (91 + 9). As rotas ainda usam `TaskRead.model_validate`: a API devolve `suggested_priority: null` até o passo 3, sem quebrar teste.

**IDs:** RF-10 (critério 2), RF-11 (critérios 1 e 2, no *service*), RF-14 (*repository* e *service*), D-05, D-06, D-07, ADR-14, ADR-16, DT-10, DT-11.

### Passo 3: rotas, tradutor do `422` e integração (RF-09, RF-10, RF-11, RF-14) — Prompt 34

**Arquivos a alterar:** `app/models/task_schemas.py`, `app/api/error_handlers.py`, `app/api/task_routes.py`, `tests/test_task_routes.py`, `docs/decisoes.md` (DT-12), `docs/arquitetura.md` (ADR-17 na tabela da seção 6), `CLAUDE.md` (linha do roteiro de checagem, abaixo).

**`app/models/task_schemas.py`** (DT-12), logo depois de `TaskDescription`:

```python
def convert_priority_text(value: object) -> object:
    """Converte o texto decimal do parâmetro de consulta em inteiro (DT-12).

    O `Literal[1, 2, 3, 4]` não aceita o texto `"1"` da *query string*. Só texto
    com dígitos decimais é convertido; o resto segue inalterado e é recusado
    pelo `Literal` com a mensagem padrão do Pydantic.

    Args:
        value: valor recebido no parâmetro.

    Returns:
        O inteiro correspondente, ou o próprio valor.
    """
    if isinstance(value, str) and value.isdecimal():
        return int(value)
    return value


TaskPriorityQuery = Annotated[TaskPriority, BeforeValidator(convert_priority_text)]
```

`TaskPriorityQuery` é usado só no parâmetro de consulta. Os corpos JSON continuam com `TaskPriority`: `{"priority": "1"}` no corpo segue respondendo `422`.

**`app/api/error_handlers.py`:**

- constante `INCOHERENT_PRIORITY_DETAIL = "Prioridade 4 (agendada) exige due_at preenchido"`, depois de `INTERNAL_ERROR_DETAIL`;
- novo tradutor, antes de `handle_database_error`:

```python
async def handle_incoherent_priority(
    request: Request, error: Exception
) -> JSONResponse:
    """Traduz `IncoherentPriorityError` em `422` com mensagem fixa (ADR-17).

    O corpo segue o formato dos outros erros de domínio (`{"detail": texto}`),
    e não o formato de lista da validação do FastAPI.

    Args:
        request: requisição que originou o erro.
        error: exceção levantada pelo `priority_advisor`.

    Returns:
        Resposta `422` com `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": INCOHERENT_PRIORITY_DETAIL},
    )
```

- em `register_error_handlers`, depois do registro de `TaskNotFoundError`: `application.add_exception_handler(IncoherentPriorityError, handle_incoherent_priority)`; a *docstring* passa a dizer "(404, 422 e 500)".

**`app/api/task_routes.py`:**

- nas rotas que devolvem `TaskRead`, trocar `TaskRead.model_validate(service.X(...))` por `service.build_task_read(service.X(...))`: `create_task`, `read_task`, `replace_task`, `patch_task` e `complete_task`. `delete_task` não muda. O tipo de retorno anotado continua `TaskRead`.
- `list_tasks` ganha o parâmetro `task_priority: Annotated[TaskPriorityQuery | None, Query(alias="priority")] = None`, depois de `task_status`, e devolve `[service.build_task_read(task) for task in service.list_tasks(task_status, task_priority)]`. *Docstring*: "Lista as tarefas por `id`, com filtros opcionais por situação e prioridade", com o argumento `task_priority: parâmetro de consulta priority (1 a 4)`.
- As rotas continuam sem capturar exceções.

**`CLAUDE.md`:** na tabela do roteiro de checagem, a linha de `status.HTTP_422_UNPROCESSABLE_ENTITY` passa a ter como substituto "`status.HTTP_422_UNPROCESSABLE_CONTENT` no código; o inteiro `422` nos testes" e como situação "proibido (Starlette 1.7.0, 05/10/2026): `StarletteDeprecationWarning`; `HTTP_422_UNPROCESSABLE_CONTENT` permitido (06/10/2026)".

**Testes** (`tests/test_task_routes.py`), ao final do arquivo. Constante:

```python
INCOHERENT_PRIORITY_RESPONSE = {
    "detail": "Prioridade 4 (agendada) exige due_at preenchido"
}
```

Os testes usam a *fixture* `client` e os auxiliares `create_task_through_api` e `PUT_BODY` da `v0.3.0`.

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_create_task_accepts_open_and_specific_tasks` | criar `title="Aberta"`; criar `title="Específica", priority=4, due_at="2026-10-10T13:00:00Z"`; `GET` de cada uma | aberta com `due_at` nulo; específica com `(priority, due_at) == (4, "2026-10-10T13:00:00Z")` |
| `test_create_task_rejects_priority_four_without_due_at_with_422` | `POST /tasks` com `{"title": "A", "priority": 4}` | `422`; `json() == INCOHERENT_PRIORITY_RESPONSE`; `GET /tasks` devolve `[]` |
| `test_replace_task_rejects_incoherent_priority_with_422` | criar; `PUT` com `{**PUT_BODY, "priority": 4}` | `422`; `INCOHERENT_PRIORITY_RESPONSE`; `GET` seguinte igual ao corpo da criação |
| `test_patch_task_rejects_incoherent_priority_with_422` | `parametrize(("create_fields", "patch_body"), ...)` com `({}, {"priority": 4})` e `({"priority": 4, "due_at": "2026-10-10T13:00:00Z"}, {"due_at": None})`; criar com `create_fields`; `PATCH` com `patch_body` | `422`; `INCOHERENT_PRIORITY_RESPONSE`; `GET` seguinte igual ao corpo da criação |
| `test_task_response_includes_suggested_priority_without_changing_priority` | `due_at = (datetime.now(UTC) + timedelta(hours=1)).isoformat()`; criar com esse `due_at`; `GET` | no `POST` e no `GET`: `(priority, suggested_priority) == (3, 1)` |
| `test_task_response_has_null_suggestion_for_open_task` | `create_task_through_api(client)` | `suggested_priority is None` |
| `test_list_tasks_filters_by_priority` | criar `("A", 1)`, `("B", 2)`, `("C", 1)`; `GET /tasks?priority=1` | títulos `["A", "C"]` |
| `test_list_tasks_combines_status_and_priority_filters` | criar `("A", 1, pending)`, `("B", 1, done)`, `("C", 2, done)`; `GET /tasks?status=done&priority=1` | títulos `["B"]` |
| `test_list_tasks_rejects_invalid_priority_with_422` | `parametrize("invalid_priority", ["0", "5", "alta"])`; `GET /tasks?priority=<valor>` | `422` em todos |
| `test_update_routes_reject_priority_outside_range_with_422` | `parametrize(("method", "json_body"), ...)` com `("PUT", {**PUT_BODY, "priority": 5})` e `("PATCH", {"priority": 0})`; criar; `client.request(method, f"/tasks/{id}", json=json_body)` | `422` em ambos |

O prazo de 1 hora do teste de sugestão usa o relógio real (o `client` usa o relógio padrão do *service*); a faixa de 4 h torna o teste estável. Os testes da `v0.3.0` continuam passando sem mudança: as tarefas deles não têm prazo ou estão concluídas, e a sugestão é igual no `POST` e no `GET` seguinte.

**Verificação:** definição de pronto; 114 testes passando (100 + 14 casos); `git status` sem `tasks.db`.

**IDs:** RF-09 (critérios 1 a 3; o 3 já coberto por `test_create_task_converts_due_at_to_utc`), RF-10 (critério 1), RF-11 (critérios 1 e 2), RF-14 (critérios 1 a 3), ADR-15, ADR-17, DT-12, RNF-08.

### Passo 4: datas no horário local (D-09, RF-09) — Prompt 34

**Arquivos a alterar:** `app/models/settings.py`, `app/models/task_schemas.py`, `app/services/task_service.py`, `app/api/task_routes.py`, `app/main.py`, `tests/test_task_service.py`, `tests/test_task_routes.py`, `docs/decisoes.md` (DT-13 a DT-15), `docs/arquitetura.md` (ADR-18 na tabela da seção 6; no ADR-10 e no ADR-15, a observação "ajustado pelo ADR-18"), `CLAUDE.md` (convenção de datas, abaixo).

**`app/models/settings.py`** (DT-14):

- `UtcOffset = Annotated[str, StringConstraints(pattern=r"^[+-](0\d|1[0-4]):[0-5]\d$")]`, depois de `Environment`;
- campo `local_utc_offset: UtcOffset = "-03:00"`, depois de `environment`;
- *docstring* da classe: as variáveis passam a ser `DATABASE_URL`, `ENVIRONMENT` e `LOCAL_UTC_OFFSET`; em `Raises`, acrescentar "ou se `LOCAL_UTC_OFFSET` não estiver no formato `±HH:MM`".

**`app/models/task_schemas.py`** (DT-13), depois de `TaskPriorityQuery`:

```python
LOCAL_DATE_TIME_FORMAT = "%d/%m/%Y %H:%M"
LOCAL_DATE_FORMAT = "%d/%m/%Y"
END_OF_DAY = time(23, 59)


def parse_local_due_at(value: object) -> object:
    """Converte `DD/MM/AAAA HH:MM` ou `DD/MM/AAAA` em data/hora local sem fuso (DT-13).

    Só data vale até o fim do dia (`END_OF_DAY`, 23:59). O fuso local é
    acrescentado pelo *service* (ADR-18). Valores que não são texto seguem
    inalterados para a validação de `NaiveDatetime`.

    Args:
        value: valor recebido em `due_at`.

    Returns:
        A data/hora sem fuso, ou o próprio valor se não for texto.

    Raises:
        ValueError: se o texto não estiver em `DD/MM/AAAA HH:MM` nem em
            `DD/MM/AAAA`, ou se a data não existir.
    """
    if not isinstance(value, str):
        return value
    try:
        return datetime.strptime(value, LOCAL_DATE_TIME_FORMAT)
    except ValueError:
        pass
    try:
        return datetime.combine(datetime.strptime(value, LOCAL_DATE_FORMAT), END_OF_DAY)
    except ValueError:
        raise ValueError(
            "use DD/MM/AAAA HH:MM, DD/MM/AAAA ou ISO 8601 com fuso horário"
        ) from None


LocalDueAt = Annotated[NaiveDatetime, BeforeValidator(parse_local_due_at)]
TaskDueAt = AwareDatetime | LocalDueAt
```

Em `TaskCreate`, `TaskUpdate` e `TaskPatch`, trocar `AwareDatetime` por `TaskDueAt` no campo `due_at`, mantendo `| None` e o padrão de cada um. Atualizar o atributo `due_at` nas três *docstrings*: "prazo em `DD/MM/AAAA HH:MM`, `DD/MM/AAAA` (até 23:59) ou ISO 8601 com fuso". `TaskRead` não muda neste passo.

**`app/services/task_service.py`** (ADR-18, DT-14):

- `TaskService.__init__(self, repository: TaskStore, clock: Callable[[], datetime] = utc_now, local_timezone: timezone = UTC) -> None`: guarda também `self.local_timezone`. O padrão `UTC` mantém o comportamento dos testes unitários existentes.
- `create_task`, depois de `ensure_priority_is_coherent`: `task_fields = task_data.model_dump()`; `task_fields["due_at"] = attach_timezone(task_data.due_at, self.local_timezone)`; `Task(**task_fields, created_at=created_at, updated_at=created_at)`.
- `replace_task`: `changes = task_data.model_dump()`; `changes["due_at"] = attach_timezone(task_data.due_at, self.local_timezone)`; `apply_changes(task, changes)`.
- `patch_task`: `changes = task_data.model_dump(exclude_unset=True)`; `if "due_at" in changes: changes["due_at"] = attach_timezone(task_data.due_at, self.local_timezone)`; `apply_changes(task, changes)`. A conferência de coerência (DT-10) continua antes, sem mudança.
- `build_task_read` passa a converter as datas para o fuso local. *Docstring*: "Monta a resposta da tarefa com a sugestão e as datas no fuso local." Corpo:

```python
        suggestion = suggest_priority(task.status, task.due_at, self.clock())
        task_read = TaskRead.model_validate(task)
        local_due_at = (
            None
            if task_read.due_at is None
            else task_read.due_at.astimezone(self.local_timezone)
        )
        return task_read.model_copy(
            update={
                "suggested_priority": suggestion,
                "due_at": local_due_at,
                "created_at": task_read.created_at.astimezone(self.local_timezone),
                "updated_at": task_read.updated_at.astimezone(self.local_timezone),
            }
        )
```

- Funções novas no módulo, antes de `build_task_service`:
  - `attach_timezone(due_at: datetime | None, local_timezone: timezone) -> datetime | None`: devolve `due_at` inalterado se for `None` ou já tiver fuso; senão, `due_at.replace(tzinfo=local_timezone)`.
  - `parse_utc_offset(utc_offset: str) -> timezone`: sinal `-1` se o texto começar com `-`, senão `1`; horas e minutos de `utc_offset[1:].split(":")`; devolve `timezone(sign * timedelta(hours=int(hours), minutes=int(minutes)))`. O formato já vem validado por `Settings`.
- `build_task_service(session: Session, utc_offset: str) -> TaskService`: devolve `TaskService(TaskRepository(session), local_timezone=parse_utc_offset(utc_offset))`.

**`app/api/task_routes.py`** (DT-15):

```python
def get_task_service(
    request: Request, session: Annotated[Session, Depends(get_db)]
) -> TaskService:
    """Dependência que compõe o *service* da requisição (ADR-14, DT-15).

    As configurações vêm de `request.app.state.settings`, gravadas por
    `create_app`, para que cada aplicação use as suas.

    Args:
        request: requisição atual.
        session: sessão aberta por `get_db`, apenas repassada ao *service*.

    Returns:
        O `TaskService` da requisição.
    """
    settings: Settings = request.app.state.settings
    return build_task_service(session, settings.local_utc_offset)
```

**`app/main.py`:** em `create_app`, antes de `application.include_router(health_router)`, a linha `application.state.settings = settings`. Nada mais muda.

**`CLAUDE.md`:** em Convenções de código, o item "Datas e horas sempre *timezone-aware* em UTC, na persistência e nos esquemas" passa a "Datas e horas sempre *timezone-aware*: em UTC na persistência; na entrada e na saída da API, no fuso local de `LOCAL_UTC_OFFSET` (ADR-18)".

**Testes que mudam** (efeito esperado da D-09; nenhum outro teste existente é alterado):

| Arquivo e teste | Mudança |
| --- | --- |
| `tests/test_task_routes.py`, `open_test_client` | novo parâmetro `local_utc_offset: str = "-03:00"`, repassado a `Settings(_env_file=None, environment=environment, local_utc_offset=local_utc_offset)`, para que os testes não dependam do ambiente da máquina |
| `test_settings_use_readme_defaults_without_environment` | também `monkeypatch.delenv("LOCAL_UTC_OFFSET", raising=False)` e `assert settings.local_utc_offset == "-03:00"` |
| `test_create_task_returns_201_with_generated_fields_and_defaults` | `created_at` termina em `"-03:00"` (antes, `"Z"`) |
| `test_create_task_converts_due_at_to_utc` | renomeado para `test_create_task_returns_due_at_in_local_offset`; envia `due_at="2026-10-10T13:00:00Z"` e espera `"2026-10-10T10:00:00-03:00"` no `POST` e no `GET` |
| `test_create_task_rejects_invalid_body_with_422` | o caso `{"title": "A", "due_at": "10/10/2026"}` passa a `{"title": "A", "due_at": "10-10-2026"}` |
| `OLD_TIMESTAMP_TEXT` | `"2019-12-31T21:00:00-03:00"` (o mesmo instante de `OLD_TIMESTAMP`, no fuso local), para que as comparações de `updated_at` continuem significativas |
| `test_create_task_accepts_open_and_specific_tasks` (passo 3) | `due_at` esperado `"2026-10-10T10:00:00-03:00"` |

**Testes novos** em `tests/test_task_service.py`, ao final. Constante `BRASILIA = timezone(timedelta(hours=-3))` depois de `REFERENCE_TIME`, e a *fixture*:

```python
@pytest.fixture
def local_service(repository: InMemoryTaskRepository) -> TaskService:
    """Service com relógio fixo e fuso local -03:00."""
    return TaskService(repository, clock=lambda: REFERENCE_TIME, local_timezone=BRASILIA)
```

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_create_task_attaches_local_timezone_to_local_due_at` | `local_service.create_task(TaskCreate(title="A", due_at="20/10/2026 14:30"))` e `TaskCreate(title="B", due_at="20/10/2026")` | `due_at == datetime(2026, 10, 20, 14, 30, tzinfo=BRASILIA)` e `datetime(2026, 10, 20, 23, 59, tzinfo=BRASILIA)` |
| `test_build_task_read_converts_dates_to_local_timezone` | criar com `due_at=datetime(2026, 10, 20, 17, 30, tzinfo=UTC)`; `build_task_read` | `due_at.utcoffset() == timedelta(hours=-3)` e `due_at.hour == 14`; `created_at` e `updated_at` com deslocamento de -3 h |
| `test_build_task_read_suggests_two_for_date_only_due_today` | criar com `due_at="10/10/2026"` (23:59 local; a referência é 09:00 local) | `suggested_priority == 2` |
| `test_parse_utc_offset_builds_fixed_timezone` | `parametrize(("utc_offset", "expected_offset"), ...)` com `("-03:00", timedelta(hours=-3))` e `("+05:30", timedelta(hours=5, minutes=30))` | `parse_utc_offset(utc_offset) == timezone(expected_offset)` |

**Testes novos** em `tests/test_task_routes.py`, ao final:

| Função | Entrada | Resultado esperado |
| --- | --- | --- |
| `test_settings_read_local_utc_offset_from_environment` | `monkeypatch.setenv("LOCAL_UTC_OFFSET", "+01:00")`; `Settings(_env_file=None)` | `local_utc_offset == "+01:00"` |
| `test_settings_reject_invalid_local_utc_offset` | `parametrize("invalid_offset", ["-3", "-03", "03:00", "-25:00", "UTC"])` no ambiente | `ValidationError` |
| `test_create_task_accepts_local_date_time` | `due_at="20/10/2026 14:30"` | `due_at == "2026-10-20T14:30:00-03:00"` |
| `test_create_task_date_only_means_end_of_day` | `priority=4`, `due_at="20/10/2026"` | `201`; `due_at == "2026-10-20T23:59:00-03:00"` |
| `test_patch_task_accepts_date_only` | criar; `PATCH {"due_at": "21/10/2026"}` | `due_at == "2026-10-21T23:59:00-03:00"` |
| `test_due_at_rejects_unsupported_formats_with_422` | `parametrize("invalid_due_at", ["2026-10-20", "2026-10-20T14:30:00", "31/02/2026", "20/10/26", "20/10/2026 14h"])` em `POST /tasks` | `422` em todos |
| `test_responses_use_configured_local_utc_offset` | `with open_test_client("test", test_engine, local_utc_offset="+01:00") as client`: criar com `due_at="20/10/2026 14:30"` | `due_at == "2026-10-20T14:30:00+01:00"`; `created_at` termina em `"+01:00"` |

**Verificação:** definição de pronto; 134 testes passando (114 + 20 casos: 5 do *service* e 15 das rotas); mypy sem erros em 18 arquivos; `git status` sem `tasks.db`.

**IDs:** D-09, RF-09 (critério 3 substituído), RNF-07, RNF-11, ADR-10, ADR-15, ADR-18, DT-13, DT-14, DT-15.

### Passo 5: exemplos de uso e configuração no README (RT-09, critério 3) — Prompt 34

**Arquivo a alterar:** `README.md`, seções Endpoints e Configuração. Sem alterar código.

1. Subir a API da raiz, sem `--reload`, com um banco temporário fora do repositório, como na `v0.3.0` (Prompt 30). PowerShell: `$env:DATABASE_URL = "sqlite:///$env:TEMP/tasks-v040.db"; python -m uvicorn app.main:app`. Apagar o arquivo antes, se existir. `LOCAL_UTC_OFFSET` fica no padrão (`-03:00`).
2. Reexecutar, na ordem da seção atual e com o banco vazio, os exemplos de tarefa já documentados, trocando nos corpos enviados o `due_at` ISO por `DD/MM/AAAA HH:MM` e cada JSON de resposta pelo novo (datas em `-03:00` e `suggested_priority`).
3. Executar e documentar quatro exemplos novos, em PowerShell e em Bash, com a resposta real:
   - `POST /tasks` com `{"title": "Consulta no dentista", "priority": 4, "due_at": "<data daqui a 14 dias, só DD/MM/AAAA>"}`: `201` com `due_at` às 23:59 local e `suggested_priority` `4`;
   - `POST /tasks` com `{"title": "Sem data", "priority": 4}`: `422` com `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`;
   - `POST /tasks` com `{"title": "A", "due_at": "2026-10-20"}`: `422` (formato não aceito);
   - `GET /tasks?priority=1` e `GET /tasks?status=pending&priority=2`: `200` com as tarefas filtradas.
4. Atualizar as tabelas da seção Endpoints: `GET /tasks` com o filtro `?priority=1` a `4`, combinável com `status`; em Tarefa, a linha de `due_at` com os três formatos aceitos e a regra das 23:59, as datas da resposta no fuso local, a linha `suggested_priority` (somente leitura, calculada a cada resposta, `null` para tarefa aberta ou concluída, nunca gravada) e a regra "prioridade `4` exige `due_at`"; em Erros, a linha do `422` de regra de negócio, com o corpo em texto; em Prioridades, a tabela de sugestão da seção 2.2 deste *blueprint*.
5. Seção Configuração: linha `LOCAL_UTC_OFFSET` (formato `±HH:MM`, padrão `-03:00`, horário de Brasília; deslocamento fixo, sem horário de verão; valor fora do formato impede a partida) e a variável no exemplo de `.env`.
6. Encerrar o servidor, remover `$env:DATABASE_URL` e apagar o banco temporário.

**Verificação:** definição de pronto (134 testes); `git status` com só o `README.md` alterado neste passo.

**IDs:** RT-09 (critério 3), RNF-07, RNF-13.

### Passo 6: fechamento (Prompt 35)

Arquivos dependentes, conforme "Fechamento de release" e "Arquivos a manter atualizados" do `CLAUDE.md`:

| Arquivo | Atualização |
| --- | --- |
| `README.md` | status (todos os requisitos funcionais implementados); Escopo do MVP sem "por exemplo" no `priority_advisor`; Roadmap com a `v0.4.0` concluída; Endpoints e Configuração conferidas; Uso de IA generativa (modelos dos Prompts 32 a 35); Limitações com o deslocamento fixo de `LOCAL_UTC_OFFSET` (sem horário de verão) e a perda da informação "só o dia" (a resposta mostra 23:59) |
| `docs/escopo-mvp.md` | D-05 a D-07 marcadas como decididas na seção 6, com o conteúdo migrado para RF-10, RF-11 e a seção 2; D-09 acrescentada à seção 6 como decidida a pedido do autor, com o conteúdo migrado para a seção 2.1 (`due_at`), o RF-09 (formatos e fuso local) e o RNF-11 (UTC na persistência, fuso local na API); RF-14 incluído na seção 3, com o critério da seção 2.1 deste *blueprint*; seção 5.2 sem "em aberto na seção 6" no filtro por prioridade; rastreabilidade (seção 7) com a contagem de testes |
| `docs/arquitetura.md` | diagrama de módulos: `priority_advisor.py` sem "(v0.4.0)", seta sólida `task_service → priority_advisor`, `priority_advisor → task_schemas` (`TaskPriority, TaskStatus`), `error_handlers → priority_advisor` (`IncoherentPriorityError`) e `task_routes → settings` (`Settings`); diagrama de `POST /tasks` com `ensure_priority_is_coherent`, o fuso local na entrada, o `422` pelo `error_handlers` e `build_task_read` com a sugestão e as datas no fuso local; diagrama de testes sem "entra na `v0.4.0`"; modelo de dados (`due_at` em UTC no banco, fuso local na API); observações e seção 4 sem decisões em aberto |
| `docs/mermaid.md` | nova seção com o antes e o depois dos diagramas alterados |
| `docs/decisoes.md` | conferir DT-09 a DT-15 |
| `docs/backlog.md` | RT-10 e RF-09 a RF-11 como `concluído`; critério 3 do RF-09 substituído pelos critérios da D-09 (seção 2.1 deste *blueprint*); RF-14 incluído na seção 4.3 como `concluído`, com 0,5 h; D-09 registrada na seção 4.3 com 1,75 h; resumo da `v0.4.0` com 5,75 h; horas reais pedidas ao autor |
| `CHANGELOG.md` | seção `0.4.0`, agrupada por tipo de *commit*, absorvendo o `[Não publicado]` |
| `docs/HISTORY-IA.md` | entradas dos Prompts 32 a 35 e consolidação da *release* |
| `prompts/Prompt 32` a `Prompt 35` | registro da execução ao final de cada arquivo |
| `docs/blueprint-v040.md` | status de executado |

Depois da aprovação do fechamento: *commits* em *Conventional Commits* na *branch* `feat/priority-advisor`, *merge* `--no-ff` em `main`, *tag* anotada `v0.4.0`, *push* (de `main`, da *tag* e da *branch*) e definição de pronto em clone limpo.

## 7. Riscos

| Risco | Tratamento |
| --- | --- |
| Teste de sugestão instável por depender do relógio | *advisor* recebe `reference_time` (ADR-16); unitários com `REFERENCE_TIME` fixo e `clocked_service`; o único teste com relógio real usa prazo de 1 h numa faixa de 4 h |
| Data sem fuso chegar ao *advisor* | entrada da API exige fuso (`AwareDatetime`), o banco devolve UTC (DT-04) e `suggest_priority` levanta `ValueError` como última barreira |
| `PATCH` deixar a tarefa incoerente, ou alterar o objeto antes de recusar | coerência no estado resultante, antes de `apply_changes` (DT-10); testes conferem `save_count == 0` e a tarefa inalterada |
| Tarefas gravadas na `v0.3.0` com prioridade 4 sem prazo | sem migração (não há dados de produção a preservar, ADR-05); o `PUT` ou `PATCH` dessas tarefas exige corrigir a combinação; a leitura, a conclusão e a exclusão continuam funcionando |
| `?priority=1` recusado pelo `Literal` | `TaskPriorityQuery` (DT-12), coberto por `test_list_tasks_filters_by_priority` |
| Mensagem de erro com detalhe interno | `422` com texto fixo (`INCOHERENT_PRIORITY_DETAIL`); o texto de `?priority=alta` vem do `Literal`, sem mensagem do `int()` |
| Sugestão confundida com a prioridade gravada | campo separado `suggested_priority`, nunca gravado; testes conferem `priority` inalterada |
| Regra de negócio na rota | rotas só chamam o *service* (`build_task_read` incluso); revisão na `v0.5.0` |
| Constante HTTP deprecada | `HTTP_422_UNPROCESSABLE_CONTENT`, verificada sem aviso (seção 3) |
| Literal de configuração no código | nenhuma configuração nova; faixas e mensagem são regra e contrato (DT-09, ADR-17) |
| `ResourceWarning` com `-W error` | nenhuma *fixture* nova abre *engine*; os testes de rota usam a `client` existente ou `open_test_client` |
| Data local interpretada no fuso errado | um único ponto de conversão no *service* (`attach_timezone` e `build_task_read`, ADR-18); teste com `LOCAL_UTC_OFFSET=+01:00` |
| Testes dependentes do ambiente da máquina (`LOCAL_UTC_OFFSET` no `.env` ou no *shell*) | `open_test_client` passa o deslocamento explícito; os testes de `Settings` usam `monkeypatch` e `_env_file=None` |
| "Só o dia" confundido com 00:00 ou com o dia seguinte | `END_OF_DAY` (23:59) e resposta no fuso local; ISO só com a data recusado (DT-13); testes no `POST` e no `PATCH` |
| Data inexistente ou formato ambíguo aceito | `strptime` recusa `31/02/2026`; `%Y` exige quatro dígitos; formatos fora dos três respondem `422` |
| Horário de verão em outra região | deslocamento fixo documentado como limitação no README (DT-14) |
| Clientes da `v0.3.0` que esperam o sufixo `Z` | mudança de contrato registrada no ADR-18 e no `CHANGELOG.md`; o ISO com fuso continua aceito na entrada |

## 8. O que não fazer

- Não criar `conftest.py`, `pyproject.toml`, `pytest.ini`, `mypy.ini`, `setup.cfg`, `Makefile` nem `.env` versionado; não criar `__init__.py` em `app/` (ADR-03) nem diretórios novos. Nenhum arquivo novo além de `app/services/priority_advisor.py`, `tests/test_priority_advisor.py` e este *blueprint*.
- Não alterar `app/models/task.py`, `app/models/base.py`, `app/models/health_schemas.py`, `app/repositories/database.py`, `app/services/health_service.py` nem `app/api/health_routes.py`. Em `app/main.py` e `app/models/settings.py`, só o que o passo 4 indica. Não criar coluna nem alterar a tabela `tasks`.
- Não usar IA, rede, serviço externo nem dependência nova no *advisor*; não alterar o `requirements.txt` (sem `tzdata`).
- Não aceitar em `due_at` formatos além dos três da D-09; não converter datas fora do *service*.
- Não gravar a sugestão nem alterar a prioridade da tarefa a partir dela.
- Não implementar paginação, ordenação configurável, busca, notificações de prazo nem filtros além de `status` e `priority`.
- Não alterar os testes da `v0.2.0` e da `v0.3.0`, salvo `InMemoryTaskRepository.find_all` (passo 2) e a tabela "Testes que mudam" do passo 4; não importar `httpx` nem `unittest.mock`.
- Não capturar exceções nas rotas nem no *repository*; não adicionar `logging.basicConfig`.
- Não alterar `docs/requerimentos.md`, `docs/PRE-HISTORY-IA.md`, `docs/EXTRA-HISTORY-IA.md`, `docs/release-review-010.md`, `docs/release-prompts-solon-020.md`, `docs/blueprint-v020.md`, `docs/blueprint-v030.md`, `LICENSE` nem `.gitignore`.
- Não comitar sem pedido.

## 9. Condição de parada

Se um passo falhar de forma não prevista (teste, mypy, aviso com `-W error`, importação), ou exigir decisão que este *blueprint* não traz, quem executa para, reporta a saída e não improvisa.

## 10. Estimativa

| Passo | Itens | Horas |
| --- | --- | --- |
| 1 | RT-10; regras de RF-10 e RF-11 | 1 |
| 2 | RF-10 (critério 2), RF-11 e RF-14 no *service* e no *repository* | 1 |
| 3 | RF-09, RF-10 (critério 1), RF-11 e RF-14 nas rotas | 1,5 |
| 4 | D-09: datas no horário local | 1,5 |
| 5 | exemplos e configuração no README | 0,75 |
| **Itens** | 3,5 h do backlog + 0,5 h do RF-14 + 1,75 h da D-09 | **5,75** |
| *Blueprint* (este arquivo) e fechamento (passo 6) | fora das estimativas dos itens | 1,5 |
| **Total da *release*** | | **7,25** |

Os 3,5 h do backlog cobrem RT-10 e RF-09 a RF-11; o RF-14 acrescenta 0,5 h (D-06) e a D-09, 1,75 h (1,5 h do passo 4 e 0,25 h a mais no README). Com 12 h reais até a `v0.3.0`, a projeção do projeto fica em cerca de 26,3 h, dentro do orçamento de cerca de 30 horas (seção 2.1, D-06).
