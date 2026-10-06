from collections.abc import Mapping
from typing import Protocol

from sqlalchemy.orm import Session

from app.models.base import utc_now
from app.models.task import Task
from app.models.task_schemas import TaskCreate, TaskPatch, TaskStatus, TaskUpdate
from app.repositories.task_repository import TaskRepository


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

    def find_all(self, status: TaskStatus | None) -> list[Task]:
        """Devolve as tarefas por `id`, filtradas por situação se informada."""
        ...

    def save(self, task: Task) -> Task:
        """Confirma as alterações de uma tarefa já carregada."""
        ...

    def delete(self, task: Task) -> None:
        """Exclui a tarefa."""
        ...


class TaskService:
    """Casos de uso de tarefas (RT-08), sem conhecimento de HTTP.

    Recebe o *repository* por injeção (ADR-14).
    """

    def __init__(self, repository: TaskStore) -> None:
        """Guarda o *repository* usado pelos casos de uso.

        Args:
            repository: persistência de tarefas.
        """
        self.repository = repository

    def create_task(self, task_data: TaskCreate) -> Task:
        """Cria uma tarefa; `created_at` e `updated_at` recebem o mesmo instante (DT-06).

        Args:
            task_data: dados validados da nova tarefa.

        Returns:
            A tarefa gravada.
        """
        created_at = utc_now()
        task = Task(
            **task_data.model_dump(), created_at=created_at, updated_at=created_at
        )
        return self.repository.add(task)

    def list_tasks(self, status: TaskStatus | None) -> list[Task]:
        """Lista as tarefas por `id`, com filtro opcional por situação.

        Args:
            status: se informado, só as tarefas com essa situação.

        Returns:
            As tarefas encontradas.
        """
        return self.repository.find_all(status)

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
        """
        task = self.get_task(task_id)
        apply_changes(task, task_data.model_dump())
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
        """
        task = self.get_task(task_id)
        apply_changes(task, task_data.model_dump(exclude_unset=True))
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


def apply_changes(task: Task, changes: Mapping[str, object]) -> None:
    """Atribui à tarefa cada campo de `changes`.

    Efeito colateral: altera `task`; não grava no banco.

    Args:
        task: tarefa a alterar.
        changes: nomes de campo e novos valores, já validados pelos esquemas.
    """
    for field_name, value in changes.items():
        setattr(task, field_name, value)


def build_task_service(session: Session) -> TaskService:
    """Compõe o *service* com o *repository* real ligado à sessão (ADR-14).

    Args:
        session: sessão da requisição.

    Returns:
        O `TaskService` pronto para uso pela rota.
    """
    return TaskService(TaskRepository(session))
