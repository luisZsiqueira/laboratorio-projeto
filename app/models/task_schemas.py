from datetime import datetime, time
from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    NaiveDatetime,
    StringConstraints,
    field_validator,
)

TaskStatus = Literal["pending", "done"]
TaskPriority = Literal[1, 2, 3, 4]

# Maior valor do INTEGER do SQLite; acima dele o driver levanta OverflowError (DT-16).
MAX_TASK_ID = 2**63 - 1
TaskId = Annotated[int, Field(le=MAX_TASK_ID)]

TaskTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]
TaskDescription = Annotated[str, StringConstraints(max_length=1000)]


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


class TaskCreate(BaseModel):
    """Corpo de `POST /tasks`.

    Campos desconhecidos ou somente leitura (`id`, `created_at`, `updated_at`)
    são rejeitados com `422`.

    Attributes:
        title: título, sem espaços nas pontas, de 1 a 200 caracteres.
        description: descrição de até 1000 caracteres, opcional.
        status: situação da tarefa; padrão `pending`.
        priority: prioridade de 1 a 4; padrão 3.
        due_at: prazo em `DD/MM/AAAA HH:MM`, `DD/MM/AAAA` (até 23:59) ou ISO 8601 com fuso, opcional.
    """

    model_config = ConfigDict(extra="forbid")

    title: TaskTitle
    description: TaskDescription | None = None
    status: TaskStatus = "pending"
    priority: TaskPriority = 3
    due_at: TaskDueAt | None = None


class TaskUpdate(BaseModel):
    """Corpo de `PUT /tasks/{task_id}`: substituição total.

    Os cinco campos são obrigatórios; `description` e `due_at` aceitam `null`,
    mas precisam estar presentes.

    Attributes:
        title: título, sem espaços nas pontas, de 1 a 200 caracteres.
        description: descrição de até 1000 caracteres, ou `null`.
        status: situação da tarefa.
        priority: prioridade de 1 a 4.
        due_at: prazo em `DD/MM/AAAA HH:MM`, `DD/MM/AAAA` (até 23:59) ou ISO 8601 com fuso, ou `null`.
    """

    model_config = ConfigDict(extra="forbid")

    title: TaskTitle
    description: TaskDescription | None
    status: TaskStatus
    priority: TaskPriority
    due_at: TaskDueAt | None


class TaskPatch(BaseModel):
    """Corpo de `PATCH /tasks/{task_id}`: alteração parcial (DT-05).

    Todos os campos são opcionais. `title`, `status` e `priority` não aceitam
    `null` explícito; `description` e `due_at` aceitam `null` para limpar o valor.

    Attributes:
        title: novo título.
        description: nova descrição, ou `null` para limpar.
        status: nova situação.
        priority: nova prioridade.
        due_at: novo prazo em `DD/MM/AAAA HH:MM`, `DD/MM/AAAA` (até 23:59) ou ISO 8601 com fuso, ou `null` para limpar.
    """

    model_config = ConfigDict(extra="forbid")

    title: TaskTitle | None = None
    description: TaskDescription | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_at: TaskDueAt | None = None

    @field_validator("title", "status", "priority")
    @classmethod
    def reject_null(cls, value: object) -> object:
        """Rejeita null explícito nos campos obrigatórios da tarefa (DT-05).

        Args:
            value: valor recebido para o campo.

        Returns:
            O próprio valor, se não for `None`.

        Raises:
            ValueError: se `value` for `None`.
        """
        if value is None:
            raise ValueError("o campo não aceita null")
        return value


class TaskRead(BaseModel):
    """Resposta dos endpoints de tarefa, construída a partir do modelo ORM.

    Attributes:
        id: identificador da tarefa.
        title: título.
        description: descrição, ou `None`.
        status: situação da tarefa.
        priority: prioridade de 1 a 4.
        due_at: prazo em UTC, ou `None`.
        created_at: instante da criação, em UTC.
        updated_at: instante da última alteração, em UTC.
        suggested_priority: prioridade sugerida pela proximidade do prazo, calculada na resposta e nunca gravada (D-07); None para tarefa aberta ou concluída.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_at: datetime | None
    created_at: datetime
    updated_at: datetime
    suggested_priority: TaskPriority | None = None
