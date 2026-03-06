"""
Configuração do banco de dados SQLite com SQLAlchemy.

Cria o engine, a sessão e a classe base para os modelos ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco SQLite – o arquivo será criado na raiz do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

# Engine SQLAlchemy; check_same_thread=False é necessário para o SQLite
# funcionar com múltiplas threads (padrão do FastAPI/uvicorn).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para todos os modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependência do FastAPI que fornece uma sessão de banco de dados
    por requisição e a fecha automaticamente ao final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
