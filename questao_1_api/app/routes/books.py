"""
Rotas (endpoints) CRUD para livros da biblioteca virtual.

Endpoints:
    POST   /livros/       – Cadastra um novo livro.
    GET    /livros/       – Lista livros, com filtro opcional por título ou autor.
    GET    /livros/{id}   – Consulta um livro pelo seu ID.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookOut

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("/", response_model=BookOut, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Cadastra um novo livro na biblioteca."""
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=List[BookOut])
def list_books(
    titulo: Optional[str] = Query(None, description="Filtrar por título (contém)"),
    autor: Optional[str] = Query(None, description="Filtrar por autor (contém)"),
    db: Session = Depends(get_db),
):
    """
    Lista todos os livros. Aceita filtros opcionais por título e/ou autor
    (busca parcial, case-insensitive).
    """
    query = db.query(Book)

    if titulo:
        query = query.filter(Book.titulo.ilike(f"%{titulo}%"))
    if autor:
        query = query.filter(Book.autor.ilike(f"%{autor}%"))

    return query.all()


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Retorna um livro pelo seu ID ou 404 se não encontrado."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book
