from datetime import UTC

import pytest

from app.models.task import Task
from app.models.task_schemas import TaskCreate, TaskPatch, TaskStatus, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService


class InMemoryTaskRepository:
    """Dublê do TaskRepository: guarda as tarefas num dicionário, sem banco (DT-07)."""

    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}
        self.save_count = 0

    def add(self, task: Task) -> Task:
        """Atribui o próximo id e guarda a tarefa."""
        task.id = len(self.tasks) + 1
        self.tasks[task.id] = task
        return task

    def get(self, task_id: int) -> Task | None:
        """Devolve a tarefa guardada ou None."""
        return self.tasks.get(task_id)

    def find_all(self, status: TaskStatus | None) -> list[Task]:
        """Devolve as tarefas por id, filtradas por status se informado."""
        return [
            task
            for task_id, task in sorted(self.tasks.items())
            if status is None or task.status == status
        ]

    def save(self, task: Task) -> Task:
        """Conta a gravação e devolve a tarefa."""
        self.save_count += 1
        return task

    def delete(self, task: Task) -> None:
        """Remove a tarefa."""
        del self.tasks[task.id]


@pytest.fixture
def repository() -> InMemoryTaskRepository:
    """Repositório em memória vazio."""
    return InMemoryTaskRepository()


@pytest.fixture
def service(repository: InMemoryTaskRepository) -> TaskService:
    """Service ligado ao repositório em memória."""
    return TaskService(repository)


def create_sample_task(service: TaskService, title: str = "Estudar FastAPI") -> Task:
    """Cria uma tarefa com os padrões do esquema."""
    return service.create_task(TaskCreate(title=title))


def build_update_body() -> TaskUpdate:
    """Corpo de substituição total usado nos testes de replace_task."""
    return TaskUpdate(
        title="B", description=None, status="done", priority=2, due_at=None
    )


def test_create_task_applies_schema_defaults(service: TaskService) -> None:
    """Criar sem campos opcionais aplica os padrões e define as datas em UTC."""
    task = create_sample_task(service)

    assert task.id == 1
    assert task.title == "Estudar FastAPI"
    assert task.description is None
    assert task.status == "pending"
    assert task.priority == 3
    assert task.due_at is None
    assert task.created_at == task.updated_at
    assert task.created_at.tzinfo is UTC


def test_list_tasks_returns_all_without_filter(service: TaskService) -> None:
    """Sem filtro, lista todas as tarefas por id."""
    create_sample_task(service, "A")
    create_sample_task(service, "B")

    assert [task.title for task in service.list_tasks(None)] == ["A", "B"]


def test_list_tasks_filters_by_status(service: TaskService) -> None:
    """Com filtro, lista só as tarefas da situação pedida."""
    create_sample_task(service, "A")
    completed_task = create_sample_task(service, "B")
    service.complete_task(completed_task.id)

    assert [task.title for task in service.list_tasks("done")] == ["B"]
    assert [task.title for task in service.list_tasks("pending")] == ["A"]


def test_get_task_returns_existing_task(service: TaskService) -> None:
    """Consultar uma tarefa existente devolve a própria tarefa."""
    task = create_sample_task(service)

    assert service.get_task(task.id) is task


def test_get_task_raises_when_missing(service: TaskService) -> None:
    """Consultar uma tarefa inexistente levanta TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError) as error_info:
        service.get_task(99)

    assert error_info.value.task_id == 99


def test_replace_task_overwrites_all_editable_fields(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """A substituição total sobrescreve os cinco campos e grava uma vez."""
    task = service.create_task(
        TaskCreate(title="A", description="antiga", priority=1)
    )

    replaced_task = service.replace_task(task.id, build_update_body())

    assert (
        replaced_task.title,
        replaced_task.description,
        replaced_task.status,
        replaced_task.priority,
    ) == ("B", None, "done", 2)
    assert repository.save_count == 1


def test_replace_task_raises_when_missing(service: TaskService) -> None:
    """Substituir uma tarefa inexistente levanta TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError):
        service.replace_task(99, build_update_body())


def test_patch_task_changes_only_sent_fields(service: TaskService) -> None:
    """A alteração parcial preserva os campos não enviados."""
    task = service.create_task(
        TaskCreate(title="A", description="mantida", priority=1)
    )

    patched_task = service.patch_task(task.id, TaskPatch(title="B"))

    assert patched_task.title == "B"
    assert patched_task.description == "mantida"
    assert patched_task.priority == 1
    assert patched_task.status == "pending"


def test_patch_task_raises_when_missing(service: TaskService) -> None:
    """Alterar parcialmente uma tarefa inexistente levanta TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError):
        service.patch_task(99, TaskPatch(title="B"))


def test_complete_task_marks_task_as_done(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """Concluir marca a tarefa como done e grava uma vez."""
    task = create_sample_task(service)

    completed_task = service.complete_task(task.id)

    assert completed_task.status == "done"
    assert repository.save_count == 1


def test_complete_task_is_idempotent(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """Concluir de novo uma tarefa concluída não grava nada."""
    task = create_sample_task(service)

    service.complete_task(task.id)
    completed_task = service.complete_task(task.id)

    assert completed_task.status == "done"
    assert repository.save_count == 1


def test_complete_task_raises_when_missing(service: TaskService) -> None:
    """Concluir uma tarefa inexistente levanta TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError):
        service.complete_task(99)


def test_delete_task_removes_task(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """Excluir remove a tarefa do repositório."""
    task = create_sample_task(service)

    service.delete_task(task.id)

    assert repository.tasks == {}


def test_delete_task_raises_when_missing(service: TaskService) -> None:
    """Excluir uma tarefa inexistente levanta TaskNotFoundError."""
    with pytest.raises(TaskNotFoundError):
        service.delete_task(99)
