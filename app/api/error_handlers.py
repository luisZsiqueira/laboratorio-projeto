import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.services.priority_advisor import IncoherentPriorityError
from app.services.task_service import TaskNotFoundError

logger = logging.getLogger(__name__)

TASK_NOT_FOUND_DETAIL = "Tarefa não encontrada"
INTERNAL_ERROR_DETAIL = "Erro interno do servidor"
INCOHERENT_PRIORITY_DETAIL = "Prioridade 4 (agendada) exige due_at preenchido"


async def handle_task_not_found(request: Request, error: Exception) -> JSONResponse:
    """Traduz `TaskNotFoundError` em `404` com mensagem fixa (ADR-15).

    O parâmetro `error` é tipado como `Exception` por exigência do contrato de
    `add_exception_handler` do Starlette. A resposta não inclui o `task_id`.

    Args:
        request: requisição que originou o erro.
        error: exceção levantada pelo *service*.

    Returns:
        Resposta `404` com `{"detail": "Tarefa não encontrada"}`.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": TASK_NOT_FOUND_DETAIL}
    )


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


async def handle_database_error(request: Request, error: Exception) -> JSONResponse:
    """Traduz falha inesperada do SQLAlchemy em `500` genérico (ADR-15).

    O detalhe da exceção vai para o log; a resposta nunca inclui a mensagem, o
    SQL nem nomes de tabela.

    Args:
        request: requisição que originou o erro.
        error: exceção do SQLAlchemy.

    Returns:
        Resposta `500` com `{"detail": "Erro interno do servidor"}`.
    """
    logger.error(
        "Falha inesperada do banco de dados em %s %s",
        request.method,
        request.url.path,
        exc_info=error,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": INTERNAL_ERROR_DETAIL},
    )


def register_error_handlers(application: FastAPI) -> None:
    """Registra na aplicação os tradutores de exceção de tarefas (404, 422 e 500).

    Args:
        application: aplicação FastAPI que recebe os tradutores.
    """
    application.add_exception_handler(TaskNotFoundError, handle_task_not_found)
    application.add_exception_handler(
        IncoherentPriorityError, handle_incoherent_priority
    )
    application.add_exception_handler(SQLAlchemyError, handle_database_error)
