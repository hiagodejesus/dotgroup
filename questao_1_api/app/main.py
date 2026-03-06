"""
Ponto de entrada da aplicação FastAPI – Biblioteca Virtual.

Cria a instância do app, registra as rotas e inicializa o banco de dados.
Executar com: uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routes.books import router as books_router

# Cria todas as tabelas no banco de dados (SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Biblioteca Virtual",
    description="API para cadastro e consulta de livros.",
    version="1.0.0",
)

# Registra as rotas de livros
app.include_router(books_router)
