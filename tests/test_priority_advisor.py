from datetime import UTC, datetime, timedelta, timezone

import pytest

from app.models.task_schemas import TaskPriority
from app.services.priority_advisor import (
    IncoherentPriorityError,
    ensure_priority_is_coherent,
    suggest_priority,
)

REFERENCE_TIME = datetime(2026, 10, 10, 12, 0, tzinfo=UTC)


def test_priority_four_without_due_at_is_incoherent() -> None:
    """Prioridade 4 sem prazo levanta a exceção, com prioridade e mensagem."""
    with pytest.raises(IncoherentPriorityError) as error_info:
        ensure_priority_is_coherent(4, None)

    assert error_info.value.priority == 4
    assert str(error_info.value) == "prioridade 4 (agendada) exige due_at preenchido"


def test_priority_four_with_due_at_is_coherent() -> None:
    """Prioridade 4 com prazo é coerente."""
    ensure_priority_is_coherent(4, REFERENCE_TIME)


@pytest.mark.parametrize("priority", [1, 2, 3])
@pytest.mark.parametrize("due_at", [None, REFERENCE_TIME])
def test_priorities_one_to_three_are_coherent_with_or_without_due_at(
    priority: TaskPriority, due_at: datetime | None
) -> None:
    """Prioridades 1 a 3 são coerentes com ou sem prazo."""
    ensure_priority_is_coherent(priority, due_at)


def test_suggest_priority_returns_none_for_open_task() -> None:
    """Tarefa aberta (sem prazo) não recebe sugestão."""
    assert suggest_priority("pending", None, REFERENCE_TIME) is None


def test_suggest_priority_returns_none_for_done_task() -> None:
    """Tarefa concluída não recebe sugestão, mesmo com prazo."""
    due_at = REFERENCE_TIME + timedelta(hours=1)

    assert suggest_priority("done", due_at, REFERENCE_TIME) is None


@pytest.mark.parametrize(
    ("remaining", "expected_priority"),
    [
        (timedelta(days=-1), 1),
        (timedelta(0), 1),
        (timedelta(hours=4), 1),
        (timedelta(hours=4, seconds=1), 2),
        (timedelta(hours=24), 2),
        (timedelta(hours=24, seconds=1), 3),
        (timedelta(days=7), 3),
        (timedelta(days=7, seconds=1), 4),
        (timedelta(days=30), 4),
    ],
)
def test_suggest_priority_by_deadline_proximity(
    remaining: timedelta, expected_priority: TaskPriority
) -> None:
    """Cada faixa e seus limites exatos; o limite fica na faixa mais urgente."""
    due_at = REFERENCE_TIME + remaining

    assert suggest_priority("pending", due_at, REFERENCE_TIME) == expected_priority


def test_suggest_priority_accepts_due_at_in_other_timezone() -> None:
    """O fuso do prazo conta: 14:00 em -03:00 são 17:00 UTC, 5 h depois da referência."""
    due_at = datetime(2026, 10, 10, 14, 0, tzinfo=timezone(timedelta(hours=-3)))

    assert suggest_priority("pending", due_at, REFERENCE_TIME) == 2


@pytest.mark.parametrize(
    ("due_at", "reference_time"),
    [
        (REFERENCE_TIME, datetime(2026, 10, 10, 12, 0)),
        (datetime(2026, 10, 11, 12, 0), REFERENCE_TIME),
    ],
)
def test_suggest_priority_rejects_naive_datetimes(
    due_at: datetime, reference_time: datetime
) -> None:
    """Data/hora sem fuso, no prazo ou na referência, levanta ValueError."""
    with pytest.raises(ValueError):
        suggest_priority("pending", due_at, reference_time)
