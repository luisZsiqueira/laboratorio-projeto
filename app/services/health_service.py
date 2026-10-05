from sqlalchemy.orm import Session

from app.models.health_schemas import HealthRead
from app.repositories.database import ping


def check_health(session: Session) -> HealthRead:
    """Verifica a saúde da aplicação a partir da resposta do banco (ADR-07).

    Não conhece HTTP nem códigos de *status*: a rota traduz o resultado.

    Args:
        session: sessão usada para consultar o banco.

    Returns:
        `HealthRead` com `ok` se o banco respondeu; `unavailable` caso contrário.
    """
    if ping(session):
        return HealthRead(status="ok", database="ok")
    return HealthRead(status="unavailable", database="unavailable")
