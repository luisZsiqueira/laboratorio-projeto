from functools import lru_cache
from typing import Annotated, Literal

from pydantic import StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "test", "production"]
UtcOffset = Annotated[str, StringConstraints(pattern=r"^[+-](0\d|1[0-4]):[0-5]\d$")]


class Settings(BaseSettings):
    """Configurações da aplicação, lidas das variáveis de ambiente e do arquivo `.env`.

    Os nomes das variáveis são `DATABASE_URL`, `ENVIRONMENT` e `LOCAL_UTC_OFFSET`
    (sem diferenciar maiúsculas de minúsculas). Os valores padrão são os do README (Configuração).
    Este é o único arquivo com literais de configuração.

    Raises:
        pydantic.ValidationError: na construção, se `ENVIRONMENT` estiver fora de
            `development`, `test` e `production`, ou se `LOCAL_UTC_OFFSET` não
            estiver no formato `±HH:MM`.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///./tasks.db"
    environment: Environment = "development"
    local_utc_offset: UtcOffset = "-03:00"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Devolve a instância única de `Settings` (uma leitura do ambiente por processo).

    Returns:
        As configurações lidas do ambiente e do `.env`.

    Raises:
        pydantic.ValidationError: se algum valor configurado for inválido.
    """
    return Settings()
