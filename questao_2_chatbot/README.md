# Questão 2 – Chatbot com IA Generativa

Chatbot interativo de linha de comando especializado em **programação Python**, construído com [LangChain](https://www.langchain.com/) e o modelo **GPT-4** da OpenAI.

O usuário faz perguntas sobre Python e recebe respostas detalhadas geradas pelo LLM, incluindo exemplos de código quando apropriado.

## Estrutura

```
questao_2_chatbot/
├── chatbot.py          # Lógica principal do chatbot (build_llm, responder, main)
├── requirements.txt    # Dependências do projeto
├── __init__.py
└── tests/
    └── test_chatbot.py # Testes unitários (sem chamadas à API real)
```

## Pré-requisitos

- Python 3.10+
- Uma chave de API da OpenAI

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Defina a variável de ambiente `OPENAI_API_KEY` antes de executar o chatbot:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

Ou crie um arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=sk-...
```

## Execução

A partir do diretório pai (`dotgroup/`):

```bash
python -m questao_2_chatbot.chatbot
```

O chatbot iniciará um loop interativo. Digite sua pergunta e pressione Enter. Para sair, digite `sair`, `exit` ou `quit`.

## Testes

Os testes utilizam **pytest** e não fazem chamadas à API real da OpenAI — usam dublês (stubs) para validar o comportamento local.

A partir do diretório pai (`dotgroup/`):

```bash
pytest questao_2_chatbot/tests/
```

Ou de dentro do diretório `questao_2_chatbot/`:

```bash
pytest tests/
```
