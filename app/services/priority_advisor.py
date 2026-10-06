from datetime import datetime, timedelta

from app.models.task_schemas import TaskPriority, TaskStatus

MANDATORY_WINDOW = timedelta(hours=4)
IMPORTANT_WINDOW = timedelta(hours=24)
REGULAR_WINDOW = timedelta(days=7)


class IncoherentPriorityError(Exception):
    """Sinaliza combinação incoerente de prioridade e prazo (D-05).

    Attributes:
        priority: prioridade recusada.
    """

    def __init__(self, priority: TaskPriority) -> None:
        """Monta a mensagem e guarda a prioridade recusada.

        Args:
            priority: prioridade que exige um prazo ausente.
        """
        super().__init__(f"prioridade {priority} (agendada) exige due_at preenchido")
        self.priority = priority


def ensure_priority_is_coherent(priority: TaskPriority, due_at: datetime | None) -> None:
    """Confere a coerência entre prioridade e prazo (D-05).

    Regra: prioridade 4 (agendada) exige `due_at`; `due_at` não exige prioridade 4.

    Args:
        priority: prioridade da tarefa.
        due_at: prazo da tarefa, ou `None` (tarefa aberta).

    Raises:
        IncoherentPriorityError: se `priority` for 4 e `due_at` for `None`.
    """
    if priority == 4 and due_at is None:
        raise IncoherentPriorityError(priority)


def suggest_priority(
    status: TaskStatus, due_at: datetime | None, reference_time: datetime
) -> TaskPriority | None:
    """Sugere a prioridade pela proximidade do prazo (D-07, DT-09).

    Sem sugestão (`None`) para tarefa concluída ou aberta. Com prazo, pelo tempo
    restante `due_at - reference_time`: até 4 h (inclusive vencido), 1; até 24 h,
    2; até 7 dias, 3; acima de 7 dias, 4. Os limites pertencem à faixa menor.

    Args:
        status: situação da tarefa.
        due_at: prazo da tarefa, com fuso horário, ou `None`.
        reference_time: instante de referência, com fuso horário.

    Returns:
        A prioridade sugerida, ou `None` se não houver base para sugerir.

    Raises:
        ValueError: se `reference_time` ou `due_at` não tiver fuso horário.
    """
    if reference_time.tzinfo is None:
        raise ValueError("a data/hora de referência precisa de fuso horário")
    if status == "done" or due_at is None:
        return None
    if due_at.tzinfo is None:
        raise ValueError("o prazo precisa de fuso horário")
    remaining = due_at - reference_time
    if remaining <= MANDATORY_WINDOW:
        return 1
    if remaining <= IMPORTANT_WINDOW:
        return 2
    if remaining <= REGULAR_WINDOW:
        return 3
    return 4
