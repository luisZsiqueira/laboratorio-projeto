import logging
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import Engine, create_engine, update
from sqlalchemy.exc import OperationalError, StatementError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.main as main_module
from app.main import create_app
from app.models.base import Base
from app.models.settings import Environment, Settings
from app.models.task import Task
from app.repositories import database
from app.repositories.database import get_db, ping
from app.repositories.task_repository import TaskRepository


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


@pytest.fixture
def task_engine(test_engine: Engine) -> Engine:
    """Engine em memória com as tabelas criadas."""
    Base.metadata.create_all(bind=test_engine)
    return test_engine


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


def test_task_dates_are_stored_in_utc_and_read_back_timezone_aware(
    task_engine: Engine,
) -> None:
    """Datas com fuso são gravadas em UTC e voltam do SQLite timezone-aware."""
    task = Task(
        title="A",
        description=None,
        status="pending",
        priority=3,
        due_at=datetime(2026, 10, 10, 10, 0, tzinfo=timezone(timedelta(hours=-3))),
    )
    with Session(task_engine) as writer_session:
        writer_session.add(task)
        writer_session.commit()
        task_id = task.id

    with Session(task_engine) as reader_session:
        stored_task = reader_session.get(Task, task_id)

        assert stored_task is not None
        assert stored_task.due_at == datetime(2026, 10, 10, 13, 0, tzinfo=UTC)
        assert stored_task.due_at is not None
        assert stored_task.due_at.tzinfo is UTC
        assert stored_task.created_at.tzinfo is UTC
        assert stored_task.updated_at.tzinfo is UTC


def test_task_rejects_naive_datetime_on_write(task_engine: Engine) -> None:
    """Data/hora sem fuso é recusada na escrita pelo tipo UTCDateTime."""
    with Session(task_engine) as session:
        session.add(
            Task(title="A", status="pending", priority=3, due_at=datetime(2026, 10, 10))
        )

        with pytest.raises(StatementError):
            session.commit()


def test_repository_add_commits_and_refreshes(task_engine: Engine) -> None:
    """add confirma a gravação e devolve a tarefa com id e datas gerados."""
    with Session(task_engine) as session:
        task = TaskRepository(session).add(
            Task(title="A", status="pending", priority=3)
        )

        assert task.id == 1
        assert task.created_at.tzinfo is UTC

    with Session(task_engine) as other_session:
        assert other_session.get(Task, 1) is not None


def test_repository_find_all_filters_by_status_in_id_order(
    task_engine: Engine,
) -> None:
    """find_all devolve por id e filtra por status quando informado."""
    with Session(task_engine) as session:
        repository = TaskRepository(session)
        for title, status in (("A", "done"), ("B", "pending"), ("C", "done")):
            repository.add(Task(title=title, status=status, priority=3))

        assert [task.title for task in repository.find_all(None)] == ["A", "B", "C"]
        assert [task.title for task in repository.find_all("done")] == ["A", "C"]


OLD_TIMESTAMP = datetime(2020, 1, 1, tzinfo=UTC)
OLD_TIMESTAMP_TEXT = "2020-01-01T00:00:00Z"
PUT_BODY = {
    "title": "B",
    "description": None,
    "status": "done",
    "priority": 2,
    "due_at": None,
}


@pytest.fixture
def broken_db_client(test_engine: Engine) -> Iterator[TestClient]:
    """Cliente cujo get_db usa um banco sem a tabela tasks (falha inesperada real)."""
    engine_without_tables = create_engine(
        "sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False}
    )
    application = create_app(Settings(_env_file=None, environment="test"), test_engine)
    application.dependency_overrides[get_db] = build_get_db_override(
        sessionmaker(bind=engine_without_tables)
    )
    try:
        with TestClient(application) as test_client:
            yield test_client
    finally:
        application.dependency_overrides.clear()
        engine_without_tables.dispose()


def create_task_through_api(client: TestClient, **fields: object) -> dict[str, object]:
    """Cria uma tarefa via POST /tasks e devolve o corpo da resposta."""
    response = client.post("/tasks", json={"title": "Estudar FastAPI", **fields})
    assert response.status_code == 201
    body: dict[str, object] = response.json()
    return body


def age_updated_at(engine: Engine, task_id: object) -> None:
    """Grava um updated_at antigo direto no banco, para comparar depois da alteração."""
    with Session(engine) as session:
        session.execute(
            update(Task).where(Task.id == task_id).values(updated_at=OLD_TIMESTAMP)
        )
        session.commit()


def test_create_task_returns_201_with_generated_fields_and_defaults(
    client: TestClient,
) -> None:
    """POST /tasks devolve 201 com id, datas e os padrões de status e prioridade."""
    task = create_task_through_api(client)

    assert task["id"] == 1
    assert task["title"] == "Estudar FastAPI"
    assert task["description"] is None
    assert task["due_at"] is None
    assert task["status"] == "pending"
    assert task["priority"] == 3
    assert str(task["created_at"]).endswith("Z")
    assert task["created_at"] == task["updated_at"]


def test_create_task_converts_due_at_to_utc(client: TestClient) -> None:
    """due_at com fuso é devolvido em UTC, na criação e na consulta seguinte."""
    task = create_task_through_api(client, due_at="2026-10-10T10:00:00-03:00")

    assert task["due_at"] == "2026-10-10T13:00:00Z"
    assert client.get(f"/tasks/{task['id']}").json()["due_at"] == "2026-10-10T13:00:00Z"


@pytest.mark.parametrize(
    "invalid_body",
    [
        {"title": ""},
        {"title": "   "},
        {"title": "x" * 201},
        {"title": "A", "description": "x" * 1001},
        {"title": "A", "status": "archived"},
        {"title": "A", "priority": 5},
        {"title": "A", "due_at": "10/10/2026"},
        {"title": "A", "due_at": "2026-10-10T10:00:00"},
        {"title": "A", "id": 7},
        {"title": "A", "created_at": "2026-10-10T10:00:00Z"},
        {"description": "sem título"},
    ],
)
def test_create_task_rejects_invalid_body_with_422(
    client: TestClient, invalid_body: dict[str, object]
) -> None:
    """Corpos inválidos ou com campos somente leitura respondem 422."""
    assert client.post("/tasks", json=invalid_body).status_code == 422


def test_create_task_accepts_title_and_description_at_maximum_length(
    client: TestClient,
) -> None:
    """Título de 200 e descrição de 1000 caracteres são aceitos."""
    task = create_task_through_api(client, title="x" * 200, description="y" * 1000)

    assert len(str(task["title"])) == 200
    assert len(str(task["description"])) == 1000


def test_list_tasks_returns_empty_list(client: TestClient) -> None:
    """Sem tarefas, GET /tasks devolve 200 e lista vazia."""
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_all_tasks_in_id_order(client: TestClient) -> None:
    """GET /tasks devolve todas as tarefas em ordem crescente de id."""
    create_task_through_api(client, title="A")
    create_task_through_api(client, title="B")

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["A", "B"]


def test_list_tasks_filters_by_status(client: TestClient) -> None:
    """O parâmetro status filtra a listagem."""
    create_task_through_api(client, title="A")
    create_task_through_api(client, title="B", status="done")

    done_titles = [task["title"] for task in client.get("/tasks?status=done").json()]
    pending_titles = [
        task["title"] for task in client.get("/tasks?status=pending").json()
    ]

    assert done_titles == ["B"]
    assert pending_titles == ["A"]


def test_list_tasks_rejects_invalid_status_with_422(client: TestClient) -> None:
    """Status fora de pending e done responde 422."""
    assert client.get("/tasks?status=archived").status_code == 422


def test_read_task_returns_existing_task(client: TestClient) -> None:
    """GET /tasks/{id} devolve a tarefa criada."""
    task = create_task_through_api(client)

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json() == task


@pytest.mark.parametrize(
    ("method", "path", "json_body"),
    [
        ("GET", "/tasks/99", None),
        ("PUT", "/tasks/99", PUT_BODY),
        ("PATCH", "/tasks/99", {"title": "B"}),
        ("POST", "/tasks/99/complete", None),
        ("DELETE", "/tasks/99", None),
    ],
)
def test_task_routes_return_404_for_missing_task(
    client: TestClient,
    method: str,
    path: str,
    json_body: dict[str, object] | None,
) -> None:
    """Todo endpoint de /tasks/{id} responde 404 com mensagem fixa."""
    response = client.request(method, path, json=json_body)

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}


def test_replace_task_overwrites_fields_and_changes_updated_at(
    client: TestClient, test_engine: Engine
) -> None:
    """PUT substitui os campos, preserva created_at e renova updated_at."""
    task = create_task_through_api(client, description="antiga", priority=1)
    age_updated_at(test_engine, task["id"])

    response = client.put(f"/tasks/{task['id']}", json=PUT_BODY)
    body = response.json()

    assert response.status_code == 200
    assert (body["title"], body["description"], body["status"], body["priority"]) == (
        "B",
        None,
        "done",
        2,
    )
    assert body["created_at"] == task["created_at"]
    assert body["updated_at"] != OLD_TIMESTAMP_TEXT


def test_replace_task_rejects_incomplete_body_with_422(client: TestClient) -> None:
    """PUT sem os cinco campos responde 422."""
    task = create_task_through_api(client)

    assert client.put(f"/tasks/{task['id']}", json={"title": "B"}).status_code == 422


def test_patch_task_changes_only_sent_fields_and_updated_at(
    client: TestClient, test_engine: Engine
) -> None:
    """PATCH altera só o que foi enviado e renova updated_at."""
    task = create_task_through_api(client, description="mantida", priority=1)
    age_updated_at(test_engine, task["id"])

    response = client.patch(f"/tasks/{task['id']}", json={"title": "B"})
    body = response.json()

    assert response.status_code == 200
    assert body["title"] == "B"
    assert body["description"] == "mantida"
    assert body["priority"] == 1
    assert body["updated_at"] != OLD_TIMESTAMP_TEXT


def test_patch_task_clears_nullable_fields(client: TestClient) -> None:
    """PATCH com null limpa description e due_at."""
    task = create_task_through_api(
        client, description="d", due_at="2026-10-10T10:00:00Z"
    )

    response = client.patch(
        f"/tasks/{task['id']}", json={"description": None, "due_at": None}
    )

    assert response.status_code == 200
    assert response.json()["description"] is None
    assert response.json()["due_at"] is None


@pytest.mark.parametrize(
    "invalid_body",
    [
        {"title": None},
        {"status": None},
        {"priority": None},
        {"title": ""},
        {"status": "archived"},
        {"id": 7},
    ],
)
def test_patch_task_rejects_invalid_body_with_422(
    client: TestClient, invalid_body: dict[str, object]
) -> None:
    """PATCH com null em campo obrigatório, valor inválido ou campo extra responde 422."""
    task = create_task_through_api(client)

    assert client.patch(f"/tasks/{task['id']}", json=invalid_body).status_code == 422


def test_complete_task_marks_done_and_is_idempotent(client: TestClient) -> None:
    """Concluir duas vezes devolve 200 nas duas e o mesmo corpo, com updated_at igual."""
    task = create_task_through_api(client)

    first_response = client.post(f"/tasks/{task['id']}/complete")
    second_response = client.post(f"/tasks/{task['id']}/complete")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json()["status"] == "done"
    assert second_response.json() == first_response.json()


def test_delete_task_returns_204_and_task_is_gone(client: TestClient) -> None:
    """DELETE devolve 204 sem corpo e a consulta seguinte devolve 404."""
    task = create_task_through_api(client)

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{task['id']}").status_code == 404


def test_task_id_must_be_integer(client: TestClient) -> None:
    """task_id que não é inteiro responde 422."""
    assert client.get("/tasks/abc").status_code == 422


def test_database_failure_returns_500_without_internal_details(
    broken_db_client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    """Falha real do banco responde 500 genérico; o detalhe vai só para o log."""
    with caplog.at_level(logging.ERROR, logger="app.api.error_handlers"):
        response = broken_db_client.get("/tasks")

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro interno do servidor"}
    assert "tasks" not in response.text
    assert "SELECT" not in response.text
    assert "no such table" in caplog.text
