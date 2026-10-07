from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.models.settings import Settings
from app.models.task_schemas import (
    TaskCreate,
    TaskId,
    TaskPatch,
    TaskPriorityQuery,
    TaskRead,
    TaskStatus,
    TaskUpdate,
)
from app.repositories.database import get_db
from app.services.task_service import TaskService, build_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

NOT_FOUND_RESPONSE: dict[int | str, dict[str, object]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Tarefa não encontrada"}
}


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


TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, service: TaskServiceDependency) -> TaskRead:
    """Cria uma tarefa.

    Args:
        task_data: corpo validado da nova tarefa.
        service: *service* de tarefas.

    Returns:
        A tarefa criada, com `201`.
    """
    return service.build_task_read(service.create_task(task_data))


@router.get("")
def list_tasks(
    service: TaskServiceDependency,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
    task_priority: Annotated[TaskPriorityQuery | None, Query(alias="priority")] = None,
) -> list[TaskRead]:
    """Lista as tarefas por `id`, com filtros opcionais por situação e prioridade.

    Args:
        service: *service* de tarefas.
        task_status: parâmetro de consulta `status` (`pending` ou `done`).
        task_priority: parâmetro de consulta `priority` (1 a 4).

    Returns:
        As tarefas encontradas.
    """
    return [
        service.build_task_read(task)
        for task in service.list_tasks(task_status, task_priority)
    ]


@router.get("/{task_id}", responses=NOT_FOUND_RESPONSE)
def read_task(task_id: TaskId, service: TaskServiceDependency) -> TaskRead:
    """Consulta uma tarefa pelo identificador.

    Args:
        task_id: identificador da tarefa.
        service: *service* de tarefas.

    Returns:
        A tarefa; `404` se não existir.
    """
    return service.build_task_read(service.get_task(task_id))


@router.put("/{task_id}", responses=NOT_FOUND_RESPONSE)
def replace_task(
    task_id: TaskId, task_data: TaskUpdate, service: TaskServiceDependency
) -> TaskRead:
    """Substitui todos os campos editáveis de uma tarefa.

    Args:
        task_id: identificador da tarefa.
        task_data: corpo completo, com os cinco campos.
        service: *service* de tarefas.

    Returns:
        A tarefa atualizada; `404` se não existir.
    """
    return service.build_task_read(service.replace_task(task_id, task_data))


@router.patch("/{task_id}", responses=NOT_FOUND_RESPONSE)
def patch_task(
    task_id: TaskId, task_data: TaskPatch, service: TaskServiceDependency
) -> TaskRead:
    """Altera só os campos enviados de uma tarefa.

    Args:
        task_id: identificador da tarefa.
        task_data: campos a alterar.
        service: *service* de tarefas.

    Returns:
        A tarefa atualizada; `404` se não existir.
    """
    return service.build_task_read(service.patch_task(task_id, task_data))


@router.post("/{task_id}/complete", responses=NOT_FOUND_RESPONSE)
def complete_task(task_id: TaskId, service: TaskServiceDependency) -> TaskRead:
    """Marca a tarefa como concluída; idempotente (D-02).

    Args:
        task_id: identificador da tarefa.
        service: *service* de tarefas.

    Returns:
        A tarefa concluída; `404` se não existir.
    """
    return service.build_task_read(service.complete_task(task_id))


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE
)
def delete_task(task_id: TaskId, service: TaskServiceDependency) -> None:
    """Exclui uma tarefa.

    Args:
        task_id: identificador da tarefa.
        service: *service* de tarefas.

    Returns:
        Nada; a resposta é `204` sem corpo, ou `404` se a tarefa não existir.
    """
    service.delete_task(task_id)
