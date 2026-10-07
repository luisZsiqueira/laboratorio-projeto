from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UTCDateTime, utc_now
from app.models.task_schemas import TaskPriority, TaskStatus


class Task(Base):
    """Modelo ORM da tarefa, tabela `tasks` (RT-05).

    O tipo da coluna é explícito: o `Literal` da anotação documenta os valores
    aceitos e o banco guarda texto e inteiro. As datas são gravadas em UTC e lidas com fuso
    (`UTCDateTime`, DT-04); `updated_at` muda a cada alteração (`onupdate`).

    Attributes:
        id: identificador gerado pelo banco.
        title: título, até 200 caracteres.
        description: descrição, até 1000 caracteres, ou `None`.
        status: situação (`pending` ou `done`).
        priority: prioridade de 1 a 4.
        due_at: prazo em UTC, ou `None`.
        created_at: instante da criação, em UTC.
        updated_at: instante da última alteração, em UTC.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[TaskStatus] = mapped_column(String(20))
    priority: Mapped[TaskPriority] = mapped_column(Integer)
    due_at: Mapped[datetime | None] = mapped_column(UTCDateTime)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime, default=utc_now, onupdate=utc_now
    )
