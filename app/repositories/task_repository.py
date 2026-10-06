from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_schemas import TaskPriority, TaskStatus


class TaskRepository:
    """Único ponto de acesso à tabela `tasks` (RT-07).

    Sem regra de negócio e só com ORM. As escritas são confirmadas aqui, com
    `commit` seguido de `refresh` (ADR-12). As exceções do SQLAlchemy não são
    capturadas: propagam até o tradutor de erro 500 da camada de rotas.
    """

    def __init__(self, session: Session) -> None:
        """Guarda a sessão usada em todas as operações.

        Args:
            session: sessão aberta (e fechada) por requisição em `get_db`.
        """
        self.session = session

    def add(self, task: Task) -> Task:
        """Grava uma tarefa nova e devolve-a com os valores gerados pelo banco.

        Args:
            task: tarefa ainda não persistida.

        Returns:
            A tarefa gravada, com `id` e datas preenchidos.
        """
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get(self, task_id: int) -> Task | None:
        """Busca uma tarefa pelo identificador.

        Args:
            task_id: identificador da tarefa.

        Returns:
            A tarefa, ou `None` se não houver linha com esse `id`.
        """
        return self.session.get(Task, task_id)

    def find_all(
        self, status: TaskStatus | None, priority: TaskPriority | None = None
    ) -> list[Task]:
        """Lista as tarefas em ordem crescente de `id`, com filtros opcionais.

        Args:
            status: se informado, devolve só as tarefas com essa situação.
            priority: se informada, devolve só as tarefas com essa prioridade.

        Returns:
            As tarefas encontradas, possivelmente uma lista vazia.
        """
        statement = select(Task).order_by(Task.id)
        if status is not None:
            statement = statement.where(Task.status == status)
        if priority is not None:
            statement = statement.where(Task.priority == priority)
        return list(self.session.scalars(statement))

    def save(self, task: Task) -> Task:
        """Confirma as alterações de uma tarefa já carregada.

        Args:
            task: tarefa carregada nesta sessão e alterada.

        Returns:
            A tarefa atualizada, com `updated_at` renovado.
        """
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        """Exclui a tarefa e confirma a exclusão.

        Args:
            task: tarefa carregada nesta sessão.
        """
        self.session.delete(task)
        self.session.commit()
