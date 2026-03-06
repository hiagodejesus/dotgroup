"""
Módulo de busca semântica utilizando embeddings e FAISS (Questão 3).

Dado um texto de consulta, gera o embedding correspondente e busca
os documentos mais similares no índice FAISS.

Execução:
    python -m questao_3_vector_store.search
"""

from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from questao_3_vector_store.embeddings import (
    INDEX_PATH,
    METADATA_PATH,
    MODEL_NAME,
    create_vector_store,
    load_index,
    load_model,
)


def semantic_search(
    query: str,
    model: SentenceTransformer,
    index,
    documents: List[str],
    top_k: int = 3,
) -> List[Tuple[str, float]]:
    """
    Realiza busca semântica: encontra os documentos mais relevantes
    para a consulta fornecida.

    Args:
        query: Texto de consulta do usuário.
        model: Modelo de embeddings já carregado.
        index: Índice FAISS com os vetores dos documentos.
        documents: Lista de textos correspondentes aos vetores.
        top_k: Quantidade de resultados a retornar.

    Returns:
        Lista de tuplas (texto_do_documento, distância) ordenada
        por relevância (menor distância = mais similar).
    """
    # Gera o embedding da consulta
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype="float32")

    # Busca os top_k vizinhos mais próximos
    distances, indices = index.search(query_embedding, top_k)

    # Monta a lista de resultados
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(documents):  # índice válido
            results.append((documents[idx], float(dist)))

    return results


def run_demo() -> None:
    """
    Demonstração da busca semântica com consultas de exemplo.

    Cria o vector store (se ainda não existir) e executa buscas
    para ilustrar o funcionamento do sistema.
    """
    # Garante que o índice existe
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        print("\u00cdndice não encontrado. Criando vector store...\n")
        create_vector_store()

    # Carrega índice e modelo
    index, documents = load_index()
    model = load_model()

    # Consultas de demonstração
    queries = [
        "Como criar uma lista em Python?",
        "Qual framework usar para criar APIs?",
        "Como funciona machine learning com Python?",
        "O que são dicionários?",
        "Como tratar erros em Python?",
    ]

    print("\n" + "=" * 70)
    print("  DEMONSTRA\u00c7\u00c3O DE BUSCA SEM\u00c2NTICA")
    print("=" * 70)

    for query in queries:
        print(f"\n\U0001f50d Consulta: \"{query}\"")
        print("-" * 60)

        results = semantic_search(query, model, index, documents, top_k=3)

        for rank, (doc, dist) in enumerate(results, start=1):
            print(f"  {rank}. [dist={dist:.4f}] {doc[:100]}...")


if __name__ == "__main__":
    run_demo()
