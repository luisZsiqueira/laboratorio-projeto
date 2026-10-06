from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.models.task_schemas import (
    TaskCreate,
    TaskPatch,
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


def get_task_service(session: Annotated[Session, Depends(get_db)]) -> TaskService:
    """Dependência que compõe o *service* com a sessão da requisição (ADR-14).

    Args:
        session: sessão aberta por `get_db`, apenas repassada ao *service*.

    Returns:
        O `TaskService` da requisição.
    """
    return build_task_service(session)


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
    return TaskRead.model_validate(service.create_task(task_data))


@router.get("")
def list_tasks(
    service: TaskServiceDependency,
    task_status: Annotated[TaskStatus | None, Query(alias="status")] = None,
) -> list[TaskRead]:
    """Lista as tarefas por `id`, com filtro opcional por situação.

    Args:
        service: *service* de tarefas.
        task_status: parâmetro de consulta `status` (`pending` ou `done`).

    Returns:
        As tarefas encontradas.
    """
    return [TaskRead.model_validate(task) for task in service.list_tasks(task_status)]


@router.get("/{task_id}", responses=NOT_FOUND_RESPONSE)
def read_task(task_id: int, service: TaskServiceDependency) -> TaskRead:
    """Consulta uma tarefa pelo identificador.

    Args:
        task_id: identificador da tarefa.
        service: *service* de tarefas.

    Returns:
        A tarefa; `404` se não existir.
    """
    return TaskRead.model_validate(service.get_task(task_id))


@router.put("/{task_id}", responses=NOT_FOUND_RESPONSE)
def replace_task(
    task_id: int, task_data: TaskUpdate, service: TaskServiceDependency
) -> TaskRead:
    """Substitui todos os campos editáveis de uma tarefa.

    Args:
        task_id: identificador da tarefa.
        task_data: corpo completo, com os cinco campos.
        service: *service* de tarefas.

    Returns:
        A tarefa atualizada; `404` se não existir.
    """
    return TaskRead.model_validate(service.replace_task(task_id, task_data))


@router.patch("/{task_id}", responses=NOT_FOUND_RESPONSE)
def patch_task(
    task_id: int, task_data: TaskPatch, service: TaskServiceDependency
) -> TaskRead:
    """Altera só os campos enviados de uma tarefa.

    Args:
        task_id: identificador da tarefa.
        task_data: campos a alterar.
        service: *service* de tarefas.

    Returns:
        A tarefa atualizada; `404` se não existir.
    """
    return TaskRead.model_validate(service.patch_task(task_id, task_data))


@router.post("/{task_id}/complete", responses=NOT_FOUND_RESPONSE)
def complete_task(task_id: int, service: TaskServiceDependency) -> TaskRead:
    """Marca a tarefa como concluída; idempotente (D-02).

    Args:
        task_id: identificador da tarefa.
        service: *service* de tarefas.

    Returns:
        A tarefa concluída; `404` se não existir.
    """
    return TaskRead.model_validate(service.complete_task(task_id))


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE
)
def delete_task(task_id: int, service: TaskServiceDependency) -> None:
    """Exclui uma tarefa.

    Args:
        task_id: identificador da tarefa.
        service: *service* de tarefas.

    Returns:
        Nada; a resposta é `204` sem corpo, ou `404` se a tarefa não existir.
    """
    service.delete_task(task_id)
