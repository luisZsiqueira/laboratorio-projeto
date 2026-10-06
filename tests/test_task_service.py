from datetime import UTC, datetime, timedelta, timezone

import pytest

from app.models.task import Task
from app.models.task_schemas import (
    TaskCreate,
    TaskPatch,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from app.services.priority_advisor import IncoherentPriorityError
from app.services.task_service import TaskNotFoundError, TaskService, parse_utc_offset

REFERENCE_TIME = datetime(2026, 10, 10, 12, 0, tzinfo=UTC)
BRASILIA = timezone(timedelta(hours=-3))


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


@pytest.fixture
def clocked_service(repository: InMemoryTaskRepository) -> TaskService:
    """Service com relógio fixo em REFERENCE_TIME, para sugestões determinísticas."""
    return TaskService(repository, clock=lambda: REFERENCE_TIME)


@pytest.fixture
def local_service(repository: InMemoryTaskRepository) -> TaskService:
    """Service com relógio fixo e fuso local -03:00."""
    return TaskService(repository, clock=lambda: REFERENCE_TIME, local_timezone=BRASILIA)


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


def test_create_task_rejects_priority_four_without_due_at(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """Prioridade 4 sem prazo levanta a exceção e nada é gravado."""
    with pytest.raises(IncoherentPriorityError):
        service.create_task(TaskCreate(title="A", priority=4))

    assert repository.tasks == {}


def test_create_task_accepts_priority_four_with_due_at(service: TaskService) -> None:
    """Prioridade 4 com prazo é gravada."""
    task = service.create_task(
        TaskCreate(title="A", priority=4, due_at=REFERENCE_TIME)
    )

    assert (task.priority, task.due_at) == (4, REFERENCE_TIME)


def test_replace_task_rejects_incoherent_priority_without_saving(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """Substituição incoerente levanta a exceção e deixa a tarefa intacta."""
    task = create_sample_task(service)

    with pytest.raises(IncoherentPriorityError):
        service.replace_task(
            task.id,
            TaskUpdate(
                title="B", description=None, status="pending", priority=4, due_at=None
            ),
        )

    assert (task.title, task.priority) == ("Estudar FastAPI", 3)
    assert repository.save_count == 0


def test_patch_task_rejects_priority_four_when_task_has_no_due_at(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """PATCH com prioridade 4 numa tarefa sem prazo é incoerente."""
    task = create_sample_task(service)

    with pytest.raises(IncoherentPriorityError):
        service.patch_task(task.id, TaskPatch(priority=4))

    assert task.priority == 3
    assert repository.save_count == 0


def test_patch_task_rejects_clearing_due_at_of_priority_four_task(
    service: TaskService, repository: InMemoryTaskRepository
) -> None:
    """PATCH com due_at nulo numa tarefa de prioridade 4 é incoerente."""
    task = service.create_task(
        TaskCreate(title="A", priority=4, due_at=REFERENCE_TIME)
    )

    with pytest.raises(IncoherentPriorityError):
        service.patch_task(task.id, TaskPatch(due_at=None))

    assert task.due_at == REFERENCE_TIME
    assert repository.save_count == 0


def test_patch_task_accepts_priority_four_with_due_at_sent_together(
    service: TaskService,
) -> None:
    """PATCH com prioridade 4 e prazo juntos é coerente."""
    task = create_sample_task(service)

    service.patch_task(task.id, TaskPatch(priority=4, due_at=REFERENCE_TIME))

    assert (task.priority, task.due_at) == (4, REFERENCE_TIME)


def test_build_task_read_includes_suggestion_without_changing_priority(
    clocked_service: TaskService,
) -> None:
    """A sugestão vai na resposta; a prioridade gravada não muda."""
    task = clocked_service.create_task(
        TaskCreate(title="A", due_at=REFERENCE_TIME + timedelta(hours=2))
    )

    task_read = clocked_service.build_task_read(task)

    assert task_read.suggested_priority == 1
    assert task_read.priority == 3
    assert task.priority == 3


def test_build_task_read_has_no_suggestion_for_open_task(
    clocked_service: TaskService,
) -> None:
    """Tarefa aberta (sem prazo) não tem sugestão."""
    task = create_sample_task(clocked_service)

    assert clocked_service.build_task_read(task).suggested_priority is None


def test_list_tasks_filters_by_priority(service: TaskService) -> None:
    """O filtro por prioridade devolve só as tarefas com ela."""
    for title, priority in [("A", 1), ("B", 2), ("C", 1)]:
        service.create_task(TaskCreate(title=title, priority=priority))

    assert [task.title for task in service.list_tasks(None, 1)] == ["A", "C"]


def test_create_task_attaches_local_timezone_to_local_due_at(
    local_service: TaskService,
) -> None:
    """Data digitada sem fuso recebe o fuso local; só o dia vale até 23:59."""
    with_time = local_service.create_task(TaskCreate(title="A", due_at="20/10/2026 14:30"))
    date_only = local_service.create_task(TaskCreate(title="B", due_at="20/10/2026"))

    assert with_time.due_at == datetime(2026, 10, 20, 14, 30, tzinfo=BRASILIA)
    assert date_only.due_at == datetime(2026, 10, 20, 23, 59, tzinfo=BRASILIA)


def test_build_task_read_converts_dates_to_local_timezone(
    local_service: TaskService,
) -> None:
    """A resposta traz due_at, created_at e updated_at no fuso local."""
    task = local_service.create_task(
        TaskCreate(title="A", due_at=datetime(2026, 10, 20, 17, 30, tzinfo=UTC))
    )

    task_read = local_service.build_task_read(task)

    assert task_read.due_at is not None
    assert task_read.due_at.utcoffset() == timedelta(hours=-3)
    assert task_read.due_at.hour == 14
    assert task_read.created_at.utcoffset() == timedelta(hours=-3)
    assert task_read.updated_at.utcoffset() == timedelta(hours=-3)


def test_build_task_read_suggests_two_for_date_only_due_today(
    local_service: TaskService,
) -> None:
    """Só o dia de hoje (23:59 local) com a referência às 09:00 local sugere 2."""
    task = local_service.create_task(TaskCreate(title="A", due_at="10/10/2026"))

    assert local_service.build_task_read(task).suggested_priority == 2


@pytest.mark.parametrize(
    ("utc_offset", "expected_offset"),
    [("-03:00", timedelta(hours=-3)), ("+05:30", timedelta(hours=5, minutes=30))],
)
def test_parse_utc_offset_builds_fixed_timezone(
    utc_offset: str, expected_offset: timedelta
) -> None:
    """O texto ±HH:MM vira um fuso fixo com o deslocamento correspondente."""
    assert parse_utc_offset(utc_offset) == timezone(expected_offset)
