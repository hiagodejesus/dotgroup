"""
Módulo de geração de embeddings e armazenamento em vector store (Questão 3).

Utiliza o modelo all-MiniLM-L6-v2 do sentence-transformers para gerar
embeddings e o FAISS para armazenar e indexar os vetores.

Fluxo:
    1. Carregar documentos de texto.
    2. Gerar embeddings para cada documento.
    3. Armazenar os embeddings em um índice FAISS.
    4. Salvar o índice e metadados em disco para uso posterior.
"""

import json
import os
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Diretório base deste módulo
BASE_DIR = Path(__file__).resolve().parent

# Caminhos padrão para o índice FAISS e metadados
INDEX_PATH = BASE_DIR / "faiss_index.bin"
METADATA_PATH = BASE_DIR / "documents_metadata.json"

# Modelo de embeddings – leve e eficiente para busca semântica
MODEL_NAME = "all-MiniLM-L6-v2"

# Documentos de exemplo (artigos curtos sobre Python)
SAMPLE_DOCUMENTS: List[str] = [
    (
        "Python é uma linguagem de programação de alto nível, interpretada e "
        "de propósito geral. Foi criada por Guido van Rossum e lançada em 1991. "
        "Python enfatiza a legibilidade do código com uso significativo de indentação."
    ),
    (
        "Listas em Python são estruturas de dados mutáveis que podem armazenar "
        "elementos de diferentes tipos. Elas suportam indexação, fatiamento "
        "e diversos métodos como append(), extend() e sort()."
    ),
    (
        "Dicionários em Python são coleções de pares chave-valor. Eles são "
        "implementados como tabelas hash e oferecem acesso em tempo constante "
        "para leitura e escrita de elementos."
    ),
    (
        "O Django é um framework web de alto nível escrito em Python que promove "
        "o desenvolvimento rápido e um design limpo e pragmático. Inclui ORM, "
        "sistema de templates e autenticação integrada."
    ),
    (
        "FastAPI é um framework web moderno para construção de APIs em Python. "
        "É baseado em type hints do Python 3.6+ e oferece validação automática, "
        "documentação interativa e alto desempenho."
    ),
    (
        "NumPy é uma biblioteca fundamental para computação científica em Python. "
        "Fornece suporte para arrays multidimensionais, funções matemáticas "
        "e ferramentas de álgebra linear."
    ),
    (
        "Machine Learning com Python utiliza bibliotecas como scikit-learn, "
        "TensorFlow e PyTorch. Essas ferramentas permitem treinar modelos "
        "de classificação, regressão e clustering com facilidade."
    ),
    (
        "Tratamento de exceções em Python é feito com blocos try/except. "
        "Isso permite capturar e tratar erros de forma elegante, evitando "
        "que o programa encerre inesperadamente."
    ),
]


def load_model(model_name: str = MODEL_NAME) -> SentenceTransformer:
    """
    Carrega o modelo de embeddings sentence-transformers.

    Args:
        model_name: Nome do modelo no HuggingFace Hub.

    Returns:
        Instância do SentenceTransformer pronta para uso.
    """
    print(f"Carregando modelo de embeddings '{model_name}'...")
    return SentenceTransformer(model_name)


def generate_embeddings(
    documents: List[str], model: SentenceTransformer
) -> np.ndarray:
    """
    Gera embeddings para uma lista de documentos.

    Args:
        documents: Lista de strings (textos dos documentos).
        model: Modelo sentence-transformers já carregado.

    Returns:
        Array NumPy de shape (n_docs, embedding_dim) com os vetores.
    """
    print(f"Gerando embeddings para {len(documents)} documentos...")
    embeddings = model.encode(documents, show_progress_bar=True)
    return np.array(embeddings, dtype="float32")


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Cria um índice FAISS (L2 / distância euclidiana) e adiciona os embeddings.

    Args:
        embeddings: Array de embeddings (float32).

    Returns:
        Índice FAISS populado.
    """
    dimension = embeddings.shape[1]
    # IndexFlatL2 faz busca exata por distância euclidiana
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"Índice FAISS criado com {index.ntotal} vetores (dim={dimension}).")
    return index


def save_index(
    index: faiss.IndexFlatL2,
    documents: List[str],
    index_path: Path = INDEX_PATH,
    metadata_path: Path = METADATA_PATH,
) -> None:
    """
    Salva o índice FAISS e os metadados (textos dos documentos) em disco.

    Args:
        index: Índice FAISS a ser salvo.
        documents: Lista original de textos (mapeamento índice → texto).
        index_path: Caminho do arquivo binário do índice.
        metadata_path: Caminho do arquivo JSON com os textos.
    """
    faiss.write_index(index, str(index_path))
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
    print(f"Índice salvo em '{index_path}' e metadados em '{metadata_path}'.")


def load_index(
    index_path: Path = INDEX_PATH,
    metadata_path: Path = METADATA_PATH,
) -> Tuple[faiss.IndexFlatL2, List[str]]:
    """
    Carrega o índice FAISS e os metadados do disco.

    Returns:
        Tupla (índice FAISS, lista de textos dos documentos).
    """
    index = faiss.read_index(str(index_path))
    with open(metadata_path, "r", encoding="utf-8") as f:
        documents = json.load(f)
    return index, documents


def create_vector_store(
    documents: List[str] = SAMPLE_DOCUMENTS,
    model_name: str = MODEL_NAME,
) -> Tuple[faiss.IndexFlatL2, List[str]]:
    """
    Pipeline completo: carrega modelo → gera embeddings → cria índice → salva.

    Args:
        documents: Documentos a serem indexados.
        model_name: Nome do modelo de embeddings.

    Returns:
        Tupla (índice FAISS, lista de documentos).
    """
    model = load_model(model_name)
    embeddings = generate_embeddings(documents, model)
    index = build_faiss_index(embeddings)
    save_index(index, documents)
    return index, documents


if __name__ == "__main__":
    # Execução direta: cria o vector store com os documentos de exemplo
    create_vector_store()
    print("\nVector store criado com sucesso!")
