import logging
from collections.abc import Iterator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.models.base import Base
from app.models.settings import get_settings

logger = logging.getLogger(__name__)


def create_db_engine(database_url: str) -> Engine:
    """Cria o engine do banco, sem conectar (ADR-04).

    O SQLite recebe `check_same_thread=False` porque as rotas síncronas rodam no
    *pool* de *threads* do FastAPI; a sessão é criada e fechada por requisição.
    Com `hide_parameters=True`, as exceções do SQLAlchemy, e portanto o log,
    trazem o SQL sem os valores enviados pelo cliente (DT-17).

    Args:
        database_url: URL de conexão do SQLAlchemy.

    Returns:
        O engine, que só conecta na primeira consulta.
    """
    return create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        hide_parameters=True,
    )


engine: Engine = create_db_engine(get_settings().database_url)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)


def get_db() -> Iterator[Session]:
    """Abre uma sessão por requisição e a fecha ao final, inclusive em erro.

    Não confirma transações: o `commit` fica no *repository* (ADR-12).

    Yields:
        A sessão aberta para a requisição.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables(db_engine: Engine) -> None:
    """Cria no banco as tabelas dos modelos que ainda não existem (ADR-05).

    Efeito colateral: grava no banco. Chamada só pelo `lifespan` de `app/main.py`.

    Args:
        db_engine: engine do banco em que as tabelas serão criadas.
    """
    Base.metadata.create_all(bind=db_engine)


def ping(session: Session) -> bool:
    """Verifica se o banco responde, executando `SELECT 1` (ADR-07).

    A exceção não é propagada: o detalhe vai para o log e a resposta HTTP não o
    revela.

    Args:
        session: sessão a ser usada na consulta.

    Returns:
        `True` se o banco respondeu; `False` se houve erro do SQLAlchemy.
    """
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Falha ao verificar a conexão com o banco de dados")
        return False
    return True
