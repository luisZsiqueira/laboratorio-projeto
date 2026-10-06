from collections.abc import Callable, Mapping
from datetime import UTC, datetime, timedelta, timezone
from typing import Protocol

from sqlalchemy.orm import Session

from app.models.base import utc_now
from app.models.task import Task
from app.models.task_schemas import (
    TaskCreate,
    TaskPatch,
    TaskPriority,
    TaskRead,
    TaskStatus,
    TaskUpdate,
)
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import ensure_priority_is_coherent, suggest_priority


class TaskNotFoundError(Exception):
    """Sinaliza que não existe tarefa com o identificador pedido.

    Attributes:
        task_id: identificador que não foi encontrado.
    """

    def __init__(self, task_id: int) -> None:
        """Monta a mensagem e guarda o identificador.

        Args:
            task_id: identificador da tarefa que não existe.
        """
        super().__init__(f"tarefa {task_id} não encontrada")
        self.task_id = task_id


class TaskStore(Protocol):
    """Contrato de persistência de tarefas exigido pelo *service* (ADR-14).

    Satisfeito estruturalmente por `TaskRepository` e por dublês de teste.
    """

    def add(self, task: Task) -> Task:
        """Grava uma tarefa nova e devolve-a."""
        ...

    def get(self, task_id: int) -> Task | None:
        """Devolve a tarefa ou `None` se não existir."""
        ...

    def find_all(
        self, status: TaskStatus | None, priority: TaskPriority | None = None
    ) -> list[Task]:
        """Devolve as tarefas por `id`, filtradas por situação e prioridade."""
        ...

    def save(self, task: Task) -> Task:
        """Confirma as alterações de uma tarefa já carregada."""
        ...

    def delete(self, task: Task) -> None:
        """Exclui a tarefa."""
        ...


class TaskService:
    """Casos de uso de tarefas (RT-08), sem conhecimento de HTTP.

    Recebe o *repository* e o relógio por injeção (ADR-14, ADR-16).
    """

    def __init__(
        self,
        repository: TaskStore,
        clock: Callable[[], datetime] = utc_now,
        local_timezone: timezone = UTC,
    ) -> None:
        """Guarda o *repository*, o relógio e o fuso local usados pelos casos de uso.

        Args:
            repository: persistência de tarefas.
            clock: devolve o instante atual com fuso, usado como referência da
                sugestão de prioridade; o padrão é `utc_now`.
            local_timezone: fuso das datas digitadas sem fuso e das datas da
                resposta (ADR-18); o padrão é UTC.
        """
        self.repository = repository
        self.clock = clock
        self.local_timezone = local_timezone

    def create_task(self, task_data: TaskCreate) -> Task:
        """Cria uma tarefa; `created_at` e `updated_at` recebem o mesmo instante (DT-06).

        Args:
            task_data: dados validados da nova tarefa.

        Returns:
            A tarefa gravada.

        Raises:
            IncoherentPriorityError: se a prioridade for 4 e não houver `due_at`.
        """
        ensure_priority_is_coherent(task_data.priority, task_data.due_at)
        created_at = utc_now()
        task_fields = task_data.model_dump()
        task_fields["due_at"] = attach_timezone(task_data.due_at, self.local_timezone)
        task = Task(**task_fields, created_at=created_at, updated_at=created_at)
        return self.repository.add(task)

    def list_tasks(
        self, status: TaskStatus | None, priority: TaskPriority | None = None
    ) -> list[Task]:
        """Lista as tarefas por `id`, com filtros opcionais por situação e prioridade.

        Args:
            status: se informado, só as tarefas com essa situação.
            priority: se informada, só as tarefas com essa prioridade.

        Returns:
            As tarefas encontradas.
        """
        return self.repository.find_all(status, priority)

    def get_task(self, task_id: int) -> Task:
        """Consulta uma tarefa pelo identificador.

        Args:
            task_id: identificador da tarefa.

        Returns:
            A tarefa encontrada.

        Raises:
            TaskNotFoundError: se não existir tarefa com esse `id`.
        """
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def replace_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        """Substitui todos os campos editáveis de uma tarefa.

        Args:
            task_id: identificador da tarefa.
            task_data: novos valores dos cinco campos.

        Returns:
            A tarefa atualizada.

        Raises:
            TaskNotFoundError: se não existir tarefa com esse `id`.
            IncoherentPriorityError: se a prioridade for 4 e `due_at` for `null`.
        """
        task = self.get_task(task_id)
        ensure_priority_is_coherent(task_data.priority, task_data.due_at)
        changes = task_data.model_dump()
        changes["due_at"] = attach_timezone(task_data.due_at, self.local_timezone)
        apply_changes(task, changes)
        return self.repository.save(task)

    def patch_task(self, task_id: int, task_data: TaskPatch) -> Task:
        """Altera só os campos enviados (DT-05); corpo vazio não altera nada.

        Args:
            task_id: identificador da tarefa.
            task_data: campos a alterar; os não enviados são preservados.

        Returns:
            A tarefa atualizada.

        Raises:
            TaskNotFoundError: se não existir tarefa com esse `id`.
            IncoherentPriorityError: se o estado resultante tiver prioridade 4
                sem `due_at` (DT-10).
        """
        task = self.get_task(task_id)
        resulting_priority = (
            task_data.priority if task_data.priority is not None else task.priority
        )
        resulting_due_at = (
            task_data.due_at if "due_at" in task_data.model_fields_set else task.due_at
        )
        ensure_priority_is_coherent(resulting_priority, resulting_due_at)
        changes = task_data.model_dump(exclude_unset=True)
        if "due_at" in changes:
            changes["due_at"] = attach_timezone(task_data.due_at, self.local_timezone)
        apply_changes(task, changes)
        return self.repository.save(task)

    def complete_task(self, task_id: int) -> Task:
        """Marca a tarefa como concluída; idempotente (D-02).

        Se a tarefa já estiver concluída, nada é gravado e `updated_at` não muda.

        Args:
            task_id: identificador da tarefa.

        Returns:
            A tarefa concluída.

        Raises:
            TaskNotFoundError: se não existir tarefa com esse `id`.
        """
        task = self.get_task(task_id)
        if task.status == "done":
            return task
        task.status = "done"
        return self.repository.save(task)

    def delete_task(self, task_id: int) -> None:
        """Exclui uma tarefa.

        Args:
            task_id: identificador da tarefa.

        Raises:
            TaskNotFoundError: se não existir tarefa com esse `id`.
        """
        self.repository.delete(self.get_task(task_id))

    def build_task_read(self, task: Task) -> TaskRead:
        """Monta a resposta da tarefa com a sugestão e as datas no fuso local.

        A sugestão usa o instante do relógio do *service* e não altera a tarefa
        nem a prioridade gravada (D-07, DT-11). As datas são convertidas para o
        fuso local (ADR-18).

        Args:
            task: tarefa carregada.

        Returns:
            O `TaskRead` com `suggested_priority` preenchido e as datas no fuso local.
        """
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


def apply_changes(task: Task, changes: Mapping[str, object]) -> None:
    """Atribui à tarefa cada campo de `changes`.

    Efeito colateral: altera `task`; não grava no banco.

    Args:
        task: tarefa a alterar.
        changes: nomes de campo e novos valores, já validados pelos esquemas.
    """
    for field_name, value in changes.items():
        setattr(task, field_name, value)


def attach_timezone(due_at: datetime | None, local_timezone: timezone) -> datetime | None:
    """Acrescenta o fuso local a uma data/hora sem fuso (ADR-18).

    Args:
        due_at: prazo recebido, ou `None`.
        local_timezone: fuso a acrescentar.

    Returns:
        `due_at` inalterado se for `None` ou já tiver fuso; senão, o mesmo
        instante de relógio no fuso local.
    """
    if due_at is None or due_at.tzinfo is not None:
        return due_at
    return due_at.replace(tzinfo=local_timezone)


def parse_utc_offset(utc_offset: str) -> timezone:
    """Converte um deslocamento `±HH:MM` em fuso fixo (DT-14).

    O formato já vem validado por `Settings`.

    Args:
        utc_offset: deslocamento em relação a UTC, por exemplo `-03:00`.

    Returns:
        O fuso com esse deslocamento.
    """
    sign = -1 if utc_offset.startswith("-") else 1
    hours, minutes = utc_offset[1:].split(":")
    return timezone(sign * timedelta(hours=int(hours), minutes=int(minutes)))


def build_task_service(session: Session, utc_offset: str) -> TaskService:
    """Compõe o *service* com o *repository* real ligado à sessão (ADR-14).

    Args:
        session: sessão da requisição.
        utc_offset: deslocamento `±HH:MM` do fuso local (`LOCAL_UTC_OFFSET`).

    Returns:
        O `TaskService` pronto para uso pela rota.
    """
    return TaskService(
        TaskRepository(session), local_timezone=parse_utc_offset(utc_offset)
    )
