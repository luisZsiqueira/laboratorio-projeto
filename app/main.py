from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine

from app.api.error_handlers import register_error_handlers
from app.api.health_routes import router as health_router
from app.api.task_routes import router as task_router
from app.models.settings import Settings, get_settings
from app.repositories.database import create_tables, engine


def create_app(settings: Settings, db_engine: Engine) -> FastAPI:
    """Compõe a aplicação FastAPI (DT-01).

    Cria as tabelas na partida (`lifespan`, ADR-05), desabilita a documentação
    interativa com `ENVIRONMENT=production` (ADR-08) e registra as rotas.

    Args:
        settings: configurações que definem o comportamento da aplicação.
        db_engine: engine em que o `lifespan` cria as tabelas.

    Returns:
        A aplicação pronta para ser servida.
    """

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        create_tables(db_engine)
        yield

    is_production = settings.environment == "production"
    application = FastAPI(
        title="To-Do List API",
        lifespan=lifespan,
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )
    application.include_router(health_router)
    application.include_router(task_router)
    register_error_handlers(application)
    return application


app = create_app(get_settings(), engine)
