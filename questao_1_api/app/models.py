"""
Modelos ORM (SQLAlchemy) para a biblioteca virtual.
"""

from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Book(Base):
    """Representa um livro na biblioteca virtual."""

    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False, index=True)
    autor = Column(String(255), nullable=False, index=True)
    data_publicacao = Column(String(20), nullable=False)   # formato livre, ex: "2024-01-15"
    resumo = Column(Text, nullable=False)
