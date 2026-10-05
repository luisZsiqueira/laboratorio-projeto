from typing import Literal

from pydantic import BaseModel

HealthStatus = Literal["ok", "unavailable"]


class HealthRead(BaseModel):
    """Resposta de `GET /health` (D-08, ADR-13).

    Attributes:
        status: situação da aplicação como um todo.
        database: situação da conexão com o banco de dados.
    """

    status: HealthStatus
    database: HealthStatus
