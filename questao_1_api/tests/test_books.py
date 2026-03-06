"""
Testes unitários para os endpoints da API de livros (Questão 1).

Utiliza o TestClient do FastAPI com um banco SQLite em memória
para garantir isolamento entre os testes.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

# ---------------------------------------------------------------------------
# Configuração: banco em memória exclusivo para os testes
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite:///./test_biblioteca.db"

engine_test = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)


def override_get_db():
    """Substitui a dependência get_db pelo banco de testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Cria as tabelas no banco de testes
Base.metadata.create_all(bind=engine_test)

client = TestClient(app)

# Payload válido reutilizado nos testes
SAMPLE_BOOK = {
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "data_publicacao": "1899-01-01",
    "resumo": "Romance que narra a história de Bentinho e Capitu.",
}


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------
def test_create_book():
    """POST /livros/ deve cadastrar um livro e retornar status 201."""
    response = client.post("/livros/", json=SAMPLE_BOOK)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == SAMPLE_BOOK["titulo"]
    assert data["autor"] == SAMPLE_BOOK["autor"]
    assert "id" in data


def test_list_books():
    """GET /livros/ deve retornar uma lista com pelo menos um livro."""
    response = client.get("/livros/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_list_books_filter_by_titulo():
    """GET /livros/?titulo=Dom deve filtrar pelo título."""
    response = client.get("/livros/", params={"titulo": "Dom"})
    assert response.status_code == 200
    data = response.json()
    assert all("Dom" in book["titulo"] for book in data)


def test_list_books_filter_by_autor():
    """GET /livros/?autor=Machado deve filtrar pelo autor."""
    response = client.get("/livros/", params={"autor": "Machado"})
    assert response.status_code == 200
    data = response.json()
    assert all("Machado" in book["autor"] for book in data)


def test_create_book_invalid_payload():
    """POST /livros/ com payload inválido deve retornar 422."""
    response = client.post("/livros/", json={"titulo": "Incompleto"})
    assert response.status_code == 422


def test_get_book_by_id():
    """GET /livros/{id} deve retornar o livro correto."""
    # Cria um livro para ter um ID conhecido
    create_resp = client.post("/livros/", json=SAMPLE_BOOK)
    book_id = create_resp.json()["id"]

    response = client.get(f"/livros/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id


def test_get_book_by_id_not_found():
    """GET /livros/{id} com ID inexistente deve retornar 404."""
    response = client.get("/livros/999999")
    assert response.status_code == 404
