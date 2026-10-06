from datetime import UTC, datetime

from sqlalchemy import DateTime, Dialect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator


class Base(DeclarativeBase):
    """Base declarativa dos modelos ORM (ADR-02).

    Importada pelos modelos e por `app/repositories/database.py`, o que evita
    ciclo de importação entre os modelos e o engine.
    """


def utc_now() -> datetime:
    """Devolve o instante atual, timezone-aware, em UTC (ADR-10).

    Returns:
        O instante atual com `tzinfo=UTC`.
    """
    return datetime.now(UTC)


class UTCDateTime(TypeDecorator[datetime]):
    """Coluna de data/hora gravada em UTC e lida como timezone-aware (ADR-10, DT-04).

    O SQLite não guarda fuso horário: na escrita, o valor é convertido para UTC
    e gravado sem fuso; na leitura, o `tzinfo=UTC` é restaurado.
    """

    impl = DateTime
    cache_ok = True

    def process_bind_param(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        """Converte a data/hora para UTC, sem fuso, antes de gravar.

        Args:
            value: data/hora a gravar, ou `None`.
            dialect: dialeto do banco (não usado).

        Returns:
            O valor em UTC sem `tzinfo`, ou `None`.

        Raises:
            ValueError: se `value` não tiver fuso horário.
        """
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("data/hora sem fuso horário não pode ser gravada")
        return value.astimezone(UTC).replace(tzinfo=None)

    def process_result_value(
        self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:
        """Restaura o fuso UTC do valor lido do banco.

        Args:
            value: data/hora lida (sem fuso), ou `None`.
            dialect: dialeto do banco (não usado).

        Returns:
            O valor com `tzinfo=UTC`, ou `None`.
        """
        if value is None:
            return None
        return value.replace(tzinfo=UTC)
