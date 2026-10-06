from datetime import datetime
from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    StringConstraints,
    field_validator,
)

TaskStatus = Literal["pending", "done"]
TaskPriority = Literal[1, 2, 3, 4]

TaskTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]
TaskDescription = Annotated[str, StringConstraints(max_length=1000)]


class TaskCreate(BaseModel):
    """Corpo de `POST /tasks`.

    Campos desconhecidos ou somente leitura (`id`, `created_at`, `updated_at`)
    são rejeitados com `422`.

    Attributes:
        title: título, sem espaços nas pontas, de 1 a 200 caracteres.
        description: descrição de até 1000 caracteres, opcional.
        status: situação da tarefa; padrão `pending`.
        priority: prioridade de 1 a 4; padrão 3.
        due_at: prazo, com fuso horário obrigatório, opcional.
    """

    model_config = ConfigDict(extra="forbid")

    title: TaskTitle
    description: TaskDescription | None = None
    status: TaskStatus = "pending"
    priority: TaskPriority = 3
    due_at: AwareDatetime | None = None


class TaskUpdate(BaseModel):
    """Corpo de `PUT /tasks/{task_id}`: substituição total.

    Os cinco campos são obrigatórios; `description` e `due_at` aceitam `null`,
    mas precisam estar presentes.

    Attributes:
        title: título, sem espaços nas pontas, de 1 a 200 caracteres.
        description: descrição de até 1000 caracteres, ou `null`.
        status: situação da tarefa.
        priority: prioridade de 1 a 4.
        due_at: prazo com fuso horário, ou `null`.
    """

    model_config = ConfigDict(extra="forbid")

    title: TaskTitle
    description: TaskDescription | None
    status: TaskStatus
    priority: TaskPriority
    due_at: AwareDatetime | None


class TaskPatch(BaseModel):
    """Corpo de `PATCH /tasks/{task_id}`: alteração parcial (DT-05).

    Todos os campos são opcionais. `title`, `status` e `priority` não aceitam
    `null` explícito; `description` e `due_at` aceitam `null` para limpar o valor.

    Attributes:
        title: novo título.
        description: nova descrição, ou `null` para limpar.
        status: nova situação.
        priority: nova prioridade.
        due_at: novo prazo com fuso horário, ou `null` para limpar.
    """

    model_config = ConfigDict(extra="forbid")

    title: TaskTitle | None = None
    description: TaskDescription | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_at: AwareDatetime | None = None

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
