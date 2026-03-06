"""
Testes para o chatbot da Questão 2.

Os testes não chamam a API real da OpenAI; em vez disso, usam dublês (stubs)
para o LLM e para a função build_llm, garantindo que o comportamento do código
local seja validado sem dependências externas.
"""
from types import SimpleNamespace

import pytest

from questao_2_chatbot import chatbot


class DummyLLM:
    """Dublê simples de ChatOpenAI, usado apenas nos testes de responder()."""

    def __init__(self, fixed_content: str) -> None:
        self.fixed_content = fixed_content
        self.last_messages = None

    def invoke(self, messages):
        # Guarda as mensagens para permitir asserts se desejado
        self.last_messages = messages
        # Simula o objeto retornado pelo ChatOpenAI, com atributo .content
        return SimpleNamespace(content=self.fixed_content)


def test_responder_returns_content():
    """responder() deve devolver exatamente o conteúdo vindo do LLM."""
    dummy = DummyLLM("Resposta de teste")
    pergunta = "Como criar uma lista em Python?"

    resultado = chatbot.responder(pergunta, dummy)

    assert resultado == "Resposta de teste"
    assert dummy.last_messages is not None
    # A última mensagem deve conter a pergunta do usuário
    assert any(pergunta in m.content for m in dummy.last_messages[1:])


def test_build_llm_without_api_key_raises(monkeypatch):
    """build_llm() deve levantar RuntimeError se OPENAI_API_KEY não estiver configurada."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        chatbot.build_llm()


def test_main_handles_missing_api_key(monkeypatch, capsys):
    """
    main() deve tratar o erro de configuração imprimindo uma mensagem amigável
    e encerrando sem lançar exceção.
    """

    def fake_build_llm():
        raise RuntimeError("OPENAI_API_KEY não configurada.")

    monkeypatch.setattr(chatbot, "build_llm", fake_build_llm)

    # Executa main(); não deve levantar exceção
    chatbot.main()

    captured = capsys.readouterr()
    assert "Erro de configuração" in captured.out

