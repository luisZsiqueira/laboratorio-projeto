import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.main as main_module
from app.main import create_app
from app.models.settings import Environment, Settings
from app.repositories import database
from app.repositories.database import get_db, ping


class FailingSession:
    """Dublê de sessão cujo execute falha como um banco indisponível (DT-03)."""

    def execute(self, *args: object, **kwargs: object) -> None:
        """Levanta OperationalError com SQL e detalhe que não podem vazar na resposta."""
        raise OperationalError("SELECT 1", {}, Exception("database is locked"))

    def close(self) -> None:
        """Não há recurso a liberar."""


class SessionSpy:
    """Dublê de sessão que registra o fechamento (DT-03)."""

    def __init__(self) -> None:
        self.is_closed = False

    def close(self) -> None:
        """Marca a sessão como fechada."""
        self.is_closed = True


@pytest.fixture
def test_engine() -> Iterator[Engine]:
    """Engine SQLite em memória compartilhado entre conexões (ADR-06)."""
    engine = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    yield engine
    engine.dispose()


def build_get_db_override(
    session_factory: sessionmaker[Session],
) -> Callable[[], Iterator[Session]]:
    """Devolve um substituto de get_db ligado ao engine de teste."""

    def override_get_db() -> Iterator[Session]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    return override_get_db


@contextmanager
def open_test_client(environment: Environment, engine: Engine) -> Iterator[TestClient]:
    """Abre um TestClient com o ambiente pedido e get_db apontando para o engine de teste."""
    application = create_app(Settings(_env_file=None, environment=environment), engine)
    application.dependency_overrides[get_db] = build_get_db_override(sessionmaker(bind=engine))
    try:
        with TestClient(application) as client:
            yield client
    finally:
        application.dependency_overrides.clear()


@pytest.fixture
def client(test_engine: Engine) -> Iterator[TestClient]:
    """Cliente de integração com ENVIRONMENT=test e banco em memória."""
    with open_test_client("test", test_engine) as test_client:
        yield test_client


@pytest.fixture
def failing_db_client(test_engine: Engine) -> Iterator[TestClient]:
    """Cliente cuja sessão de banco falha em toda consulta."""
    application = create_app(Settings(_env_file=None, environment="test"), test_engine)

    def override_get_db() -> Iterator[FailingSession]:
        yield FailingSession()

    application.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(application) as test_client:
            yield test_client
    finally:
        application.dependency_overrides.clear()


def test_settings_use_readme_defaults_without_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sem variáveis de ambiente nem .env, valem os padrões do README."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    settings = Settings(_env_file=None)

    assert settings.database_url == "sqlite:///./tasks.db"
    assert settings.environment == "development"


def test_settings_read_values_from_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """As variáveis de ambiente substituem os padrões."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./outro.db")
    monkeypatch.setenv("ENVIRONMENT", "production")

    settings = Settings(_env_file=None)

    assert settings.database_url == "sqlite:///./outro.db"
    assert settings.environment == "production"


def test_settings_read_values_from_env_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Os valores do arquivo .env são lidos quando não há variáveis de ambiente."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DATABASE_URL=sqlite:///./arquivo.db\nENVIRONMENT=test\n", encoding="utf-8"
    )

    settings = Settings(_env_file=env_file)

    assert settings.database_url == "sqlite:///./arquivo.db"
    assert settings.environment == "test"


def test_settings_reject_environment_outside_allowed_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """ENVIRONMENT fora do conjunto aceito levanta ValidationError."""
    monkeypatch.setenv("ENVIRONMENT", "staging")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_get_db_closes_session_after_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A sessão entregue por get_db é fechada quando a requisição termina."""
    spy = SessionSpy()
    monkeypatch.setattr(database, "SessionLocal", lambda: spy)

    generator = get_db()
    assert next(generator) is spy
    with pytest.raises(StopIteration):
        next(generator)

    assert spy.is_closed


def test_get_db_closes_session_when_request_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A sessão é fechada mesmo quando a requisição levanta exceção."""
    spy = SessionSpy()
    monkeypatch.setattr(database, "SessionLocal", lambda: spy)

    generator = get_db()
    next(generator)
    with pytest.raises(RuntimeError):
        generator.throw(RuntimeError("falha simulada"))

    assert spy.is_closed


def test_ping_returns_true_when_database_is_available(test_engine: Engine) -> None:
    """Com o banco disponível, ping devolve True."""
    with Session(test_engine) as session:
        assert ping(session) is True


def test_ping_returns_false_and_logs_when_database_fails(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Com o banco falhando, ping devolve False e registra o detalhe no log."""
    with caplog.at_level(logging.ERROR, logger="app.repositories.database"):
        result = ping(FailingSession())

    assert result is False
    assert "database is locked" in caplog.text


def test_lifespan_creates_tables_on_startup(
    monkeypatch: pytest.MonkeyPatch, test_engine: Engine
) -> None:
    """O lifespan chama create_tables com o engine recebido por create_app."""
    created_on: list[Engine] = []
    monkeypatch.setattr(main_module, "create_tables", created_on.append)
    application = create_app(Settings(_env_file=None, environment="test"), test_engine)

    with TestClient(application):
        pass

    assert created_on == [test_engine]


def test_health_returns_200_when_database_is_available(client: TestClient) -> None:
    """Com o banco disponível, /health responde 200 com status ok."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_returns_503_without_internal_details_when_database_fails(
    failing_db_client: TestClient,
) -> None:
    """Com o banco falhando, /health responde 503 sem SQL, exceção nem stack trace."""
    response = failing_db_client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": "unavailable"}
    assert "SELECT" not in response.text
    assert "Traceback" not in response.text
    assert "locked" not in response.text


def test_docs_available_in_development(test_engine: Engine) -> None:
    """Em development, /docs e /openapi.json estão disponíveis."""
    with open_test_client("development", test_engine) as development_client:
        assert development_client.get("/docs").status_code == 200
        assert development_client.get("/openapi.json").status_code == 200


def test_docs_disabled_in_production(test_engine: Engine) -> None:
    """Em production, /docs, /redoc e /openapi.json respondem 404."""
    with open_test_client("production", test_engine) as production_client:
        assert production_client.get("/docs").status_code == 404
        assert production_client.get("/redoc").status_code == 404
        assert production_client.get("/openapi.json").status_code == 404
