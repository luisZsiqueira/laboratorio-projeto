from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa dos modelos ORM (ADR-02).

    Importada pelos modelos e por `app/repositories/database.py`, o que evita
    ciclo de importação entre os modelos e o engine.
    """
