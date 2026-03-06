"""
Testes unitários para o sistema de busca semântica (Questão 3).

Valida a geração de embeddings, a construção do índice FAISS,
a persistência em disco e a função de busca semântica.
"""

import sys
from pathlib import Path

# Garante que o diretório-pai esteja no sys.path para que os imports
# "from questao_3_vector_store.…" funcionem corretamente.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np
import pytest

from questao_3_vector_store.embeddings import (
    SAMPLE_DOCUMENTS,
    build_faiss_index,
    generate_embeddings,
    load_index,
    load_model,
    save_index,
)
from questao_3_vector_store.search import semantic_search


# ---------------------------------------------------------------------------
# Fixtures (modelo e embeddings são caros; reutilizamos por sessão)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def model():
    """Carrega o modelo de embeddings uma única vez por sessão de testes."""
    return load_model()


@pytest.fixture(scope="session")
def embeddings(model):
    """Gera embeddings para os documentos de exemplo uma única vez."""
    return generate_embeddings(SAMPLE_DOCUMENTS, model)


@pytest.fixture(scope="session")
def faiss_index(embeddings):
    """Constrói o índice FAISS uma única vez."""
    return build_faiss_index(embeddings)


# ---------------------------------------------------------------------------
# Testes – Embeddings
# ---------------------------------------------------------------------------
def test_load_model(model):
    """O modelo deve ser carregado com sucesso."""
    assert model is not None


def test_generate_embeddings_shape(embeddings):
    """Os embeddings devem ter shape (n_documentos, dimensão_do_modelo)."""
    n_docs = len(SAMPLE_DOCUMENTS)
    assert embeddings.shape[0] == n_docs
    # all-MiniLM-L6-v2 produz vetores de dimensão 384
    assert embeddings.shape[1] == 384


def test_generate_embeddings_dtype(embeddings):
    """Os embeddings devem ser do tipo float32 (exigido pelo FAISS)."""
    assert embeddings.dtype == np.float32


def test_embeddings_are_not_identical(embeddings):
    """Documentos diferentes devem gerar embeddings diferentes."""
    # Compara o primeiro e o segundo documento
    assert not np.allclose(embeddings[0], embeddings[1])


# ---------------------------------------------------------------------------
# Testes – Índice FAISS
# ---------------------------------------------------------------------------
def test_build_faiss_index_count(faiss_index):
    """O índice deve conter exatamente o número de documentos indexados."""
    assert faiss_index.ntotal == len(SAMPLE_DOCUMENTS)


def test_faiss_index_dimension(faiss_index):
    """A dimensão do índice deve corresponder à do modelo (384)."""
    assert faiss_index.d == 384


# ---------------------------------------------------------------------------
# Testes – Persistência (save / load)
# ---------------------------------------------------------------------------
def test_save_and_load_index(faiss_index, tmp_path):
    """Salvar e recarregar o índice deve preservar os dados."""
    index_path = tmp_path / "test_index.bin"
    metadata_path = tmp_path / "test_metadata.json"

    save_index(faiss_index, SAMPLE_DOCUMENTS, index_path, metadata_path)

    loaded_index, loaded_docs = load_index(index_path, metadata_path)

    assert loaded_index.ntotal == faiss_index.ntotal
    assert loaded_docs == SAMPLE_DOCUMENTS


# ---------------------------------------------------------------------------
# Testes – Busca Semântica
# ---------------------------------------------------------------------------
def test_semantic_search_returns_results(model, faiss_index):
    """A busca deve retornar a quantidade solicitada de resultados."""
    results = semantic_search(
        "Como criar uma lista em Python?",
        model,
        faiss_index,
        SAMPLE_DOCUMENTS,
        top_k=3,
    )
    assert len(results) == 3


def test_semantic_search_result_format(model, faiss_index):
    """Cada resultado deve ser uma tupla (texto, distância)."""
    results = semantic_search(
        "O que é Python?",
        model,
        faiss_index,
        SAMPLE_DOCUMENTS,
        top_k=1,
    )
    text, distance = results[0]
    assert isinstance(text, str)
    assert isinstance(distance, float)
    assert distance >= 0.0


def test_semantic_search_relevance_listas(model, faiss_index):
    """Uma consulta sobre listas deve retornar o documento de listas como top-1."""
    results = semantic_search(
        "Listas mutáveis com append e sort em Python",
        model,
        faiss_index,
        SAMPLE_DOCUMENTS,
        top_k=1,
    )
    top_doc, _ = results[0]
    # O documento mais relevante deve mencionar "Listas"
    assert "Listas" in top_doc or "lista" in top_doc.lower()


def test_semantic_search_relevance_machine_learning(model, faiss_index):
    """Uma consulta sobre ML deve retornar o documento de Machine Learning."""
    results = semantic_search(
        "machine learning e inteligência artificial",
        model,
        faiss_index,
        SAMPLE_DOCUMENTS,
        top_k=1,
    )
    top_doc, _ = results[0]
    assert "Machine Learning" in top_doc


def test_semantic_search_distances_sorted(model, faiss_index):
    """Os resultados devem estar ordenados por distância crescente."""
    results = semantic_search(
        "frameworks web em Python",
        model,
        faiss_index,
        SAMPLE_DOCUMENTS,
        top_k=5,
    )
    distances = [dist for _, dist in results]
    assert distances == sorted(distances)
