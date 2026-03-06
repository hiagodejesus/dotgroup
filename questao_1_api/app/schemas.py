"""
Schemas Pydantic (v1) para validação e serialização dos dados de livros.
"""

from pydantic import BaseModel


class BookCreate(BaseModel):
    """Schema para criação de um livro (entrada)."""

    titulo: str
    autor: str
    data_publicacao: str
    resumo: str


class BookOut(BookCreate):
    """Schema de resposta, inclui o id gerado pelo banco."""

    id: int

    class Config:
        # Permite que o Pydantic leia dados de objetos ORM do SQLAlchemy
        orm_mode = True
