# Questão 3 – Busca Semântica com Embeddings e Vector Store

Módulo que implementa um sistema de **busca semântica** utilizando embeddings gerados pelo modelo [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (sentence-transformers) e indexados com [FAISS](https://github.com/facebookresearch/faiss).

## Estrutura do Projeto

```
questao_3_vector_store/
├── embeddings.py          # Geração de embeddings e gerenciamento do índice FAISS
├── search.py              # Busca semântica sobre o índice
├── requirements.txt       # Dependências do projeto
├── __init__.py            # Inicialização do pacote
├── documents/             # Diretório para documentos auxiliares
├── tests/
│   └── test_vector_store.py  # Testes unitários (pytest)
```

## Como Funciona

1. **Geração de embeddings** – Textos de exemplo sobre Python são convertidos em vetores de 384 dimensões pelo modelo `all-MiniLM-L6-v2`.
2. **Indexação** – Os vetores são armazenados em um índice FAISS (`IndexFlatL2`), que realiza busca exata por distância euclidiana.
3. **Persistência** – O índice e os metadados (textos originais) são salvos em disco (`faiss_index.bin` e `documents_metadata.json`).
4. **Busca semântica** – Dada uma consulta, o sistema gera o embedding correspondente e retorna os documentos mais similares.

## Instalação

```bash
pip install -r requirements.txt
```

### Dependências principais

- `sentence-transformers` – Modelo de embeddings
- `faiss-cpu` – Vector store / busca por similaridade
- `numpy` – Operações com arrays
- `pytest` – Framework de testes

## Uso

### Criar o vector store

```bash
python -m questao_3_vector_store.embeddings
```

Isso gera os arquivos `faiss_index.bin` e `documents_metadata.json` no diretório do módulo.

### Executar a demonstração de busca semântica

```bash
python -m questao_3_vector_store.search
```

Executa buscas de exemplo e exibe os documentos mais relevantes para cada consulta.

## Testes

Os testes utilizam **pytest** e cobrem:

- Carregamento do modelo de embeddings
- Shape e tipo dos vetores gerados
- Construção e dimensão do índice FAISS
- Persistência (salvar e carregar o índice)
- Resultados da busca semântica (formato, relevância e ordenação)

### Executar os testes

A partir do diretório **pai** do módulo (`dotgroup/`):

```bash
pytest questao_3_vector_store/tests/ -v
```

Ou diretamente de dentro do módulo:

```bash
pytest tests/ -v
```

> **Nota:** a primeira execução pode ser mais lenta, pois o modelo `all-MiniLM-L6-v2` será baixado automaticamente pelo sentence-transformers.
