"""
Chatbot de Python com IA Generativa (Questão 2).

Utiliza o Langchain para orquestrar a conversa com o modelo GPT-4 da OpenAI.
O usuário faz perguntas sobre programação em Python e recebe respostas
detalhadas geradas pelo LLM.

Execução:
    export OPENAI_API_KEY="sk-..."
    python -m questao_2_chatbot.chatbot
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Carrega variáveis de ambiente de um arquivo .env, se existir
load_dotenv()

# Mensagem de sistema que define o comportamento do chatbot
SYSTEM_PROMPT = (
    "Você é um assistente especialista em programação Python. "
    "Responda de forma clara, com exemplos de código quando apropriado."
)


def build_llm() -> ChatOpenAI:
    """
    Constrói e retorna uma instância de ChatOpenAI (GPT-4).

    Raises:
        RuntimeError: Se a variável de ambiente OPENAI_API_KEY não estiver
                      configurada.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY não configurada. "
            "Defina a variável de ambiente antes de executar o chatbot."
        )

    return ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        openai_api_key=api_key,
    )


def responder(pergunta: str, llm) -> str:
    """
    Envia uma pergunta ao LLM e retorna a resposta como string.

    Args:
        pergunta: Texto da pergunta do usuário.
        llm: Instância do modelo de linguagem (ex: ChatOpenAI).

    Returns:
        Texto da resposta gerada pelo modelo.
    """
    # Monta a lista de mensagens: sistema + pergunta do usuário
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=pergunta),
    ]

    # Invoca o modelo e extrai o conteúdo da resposta
    resultado = llm.invoke(messages)
    return resultado.content


def main() -> None:
    """
    Loop principal do chatbot.

    Exemplos de perguntas:
        - "Como criar uma lista em Python?"
        - "Explique list comprehensions."
        - "Como ler um arquivo JSON em Python?"
    """
    try:
        llm = build_llm()
    except RuntimeError as exc:
        print(f"Erro de configuração: {exc}")
        return

    print("=" * 60)
    print("  Chatbot Python – Pergunte sobre programação em Python!")
    print("  Digite 'sair' para encerrar.")
    print("=" * 60)

    while True:
        pergunta = input("\nVocê: ").strip()
        if not pergunta:
            continue
        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Até mais!")
            break

        resposta = responder(pergunta, llm)
        print(f"\nBot: {resposta}")


if __name__ == "__main__":
    main()
