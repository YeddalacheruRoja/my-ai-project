from types import SimpleNamespace

import pytest
from fastapi import HTTPException

import main
from main import RAGRequest, retrieve_documents


def test_retrieve_documents_ranks_matching_context():
    documents = [
        "Oranges are citrus fruit.",
        "Python is a programming language.",
        "Python supports programming with readable syntax.",
    ]

    result = retrieve_documents("Python programming", documents, top_k=1)

    assert result == ["Python is a programming language."]


def test_retrieve_documents_returns_empty_for_no_match():
    assert retrieve_documents("volcano", ["Ocean currents move heat."], top_k=3) == []


def test_rag_endpoint_returns_generated_answer_and_sources(monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            assert "Python is a programming language." in kwargs["messages"][1]["content"]
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="Python is a language."))]
            )

    class FakeOpenAI:
        def __init__(self, api_key):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(main, "OpenAI", FakeOpenAI)

    response = main.rag_endpoint(
        RAGRequest(query="Python language", documents=["Python is a programming language."])
    )

    assert response.answer == "Python is a language."
    assert response.sources == ["Python is a programming language."]


def test_rag_endpoint_requires_provider_configuration(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(HTTPException) as error:
        main.rag_endpoint(RAGRequest(query="Python language", documents=["Python is a language."]))

    assert error.value.status_code == 503