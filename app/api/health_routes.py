from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.models.health_schemas import HealthRead
from app.repositories.database import get_db
from app.services.health_service import check_health

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthRead,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": HealthRead}},
)
def read_health(
    response: Response, session: Annotated[Session, Depends(get_db)]
) -> HealthRead:
    """Informa se a aplicação e o banco de dados estão disponíveis.

    Args:
        response: resposta HTTP, usada para definir o código de *status*.
        session: sessão do banco, repassada ao *service*.

    Returns:
        `HealthRead`; o código é `200` com o banco disponível e `503` sem ele.
    """
    health = check_health(session)
    if health.status == "unavailable":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return health
