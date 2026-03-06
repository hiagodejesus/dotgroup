# Biblioteca Virtual – API (Questão 1)

API REST para cadastro e consulta de livros, construída com **FastAPI**, **SQLAlchemy** e **SQLite**.

## Estrutura do Projeto

```
questao_1_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Ponto de entrada da aplicação FastAPI
│   ├── database.py      # Configuração do engine e sessão SQLAlchemy (SQLite)
│   ├── models.py        # Modelo ORM "Book" (tabela livros)
│   ├── schemas.py       # Schemas Pydantic para validação de entrada/saída
│   └── routes/
│       ├── __init__.py
│       └── books.py     # Endpoints CRUD de livros
├── tests/
│   ├── __init__.py
│   └── test_books.py    # Testes unitários dos endpoints
├── requirements.txt
└── README.md
```

## Endpoints

| Método | Rota             | Descrição                                        |
|--------|------------------|--------------------------------------------------|
| POST   | `/livros/`       | Cadastra um novo livro                           |
| GET    | `/livros/`       | Lista livros (filtros opcionais: `titulo`, `autor`) |
| GET    | `/livros/{id}`   | Consulta um livro pelo ID                        |

## Pré-requisitos

- Python 3.10+

## Instalação

1. Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Executando a aplicação

```powershell
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger) pode ser acessada em `http://127.0.0.1:8000/docs`.

## Executando os testes

Os testes utilizam **pytest** com o `TestClient` do FastAPI e um banco SQLite separado (`test_biblioteca.db`) para isolamento.

```powershell
pytest
```

Para ver a saída detalhada:

```powershell
pytest -v
```
