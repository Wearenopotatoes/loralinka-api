import os
from pathlib import Path
from typing import Generator, Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def _build_database_url() -> str:
    """
    Obtiene la URL de conexión:
    - Usa DATABASE_URL si está definida.
    - Si no, la construye con:
      DB_DIALECT, DB_DRIVER (opcional), DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
    - Fallback a SQLite local si no hay datos suficientes.
    """
    direct = os.getenv("DATABASE_URL")
    if direct:
        return direct.strip().strip('"').strip("'")

    dialect = (os.getenv("DB_DIALECT") or "postgresql").strip()
    driver = (os.getenv("DB_DRIVER") or "psycopg2").strip()
    user = (os.getenv("DB_USER") or "").strip()
    password = (os.getenv("DB_PASSWORD") or "").strip()
    host = (os.getenv("DB_HOST") or "").strip()
    port = (os.getenv("DB_PORT") or "").strip()
    name = (os.getenv("DB_NAME") or "").strip()

    # Defaults y validaciones para PostgreSQL
    if not port:
        port = "5432"
    if not all([user, host, name]):
        raise ValueError("Faltan variables para PostgreSQL: DB_USER, DB_HOST, DB_NAME")

    dialect_driver = f"{dialect}+{driver}" if driver else dialect

    from urllib.parse import quote_plus
    pw = quote_plus(password) if password else ""

    auth = user
    if pw:
        auth = f"{user}:{pw}"
    if auth:
        auth = f"{auth}@"

    netloc = host
    if port:
        netloc = f"{host}:{port}"

    return f"{dialect_driver}://{auth}{netloc}/{name}"


# Cargar .env ubicado en la raíz de src
SRC_DIR = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=SRC_DIR / ".env", override=False)

# Crear engine, SessionLocal y dependencia de DB
DATABASE_URL = _build_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=os.getenv("SQL_ECHO", "0").lower() in ("1", "true", "yes"),
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para FastAPI: abre una sesión y la cierra al finalizar.
    Uso:
        def endpoint(db: DbSession): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Alias de tipo para inyectar la sesión en endpoints de FastAPI
DbSession = Annotated[Session, Depends(get_db)]
