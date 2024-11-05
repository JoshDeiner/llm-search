import pytest
from llm_core.llm_provider import LLMProvider


@pytest.fixture
def llm_provider():
    return LLMProvider(model_name="gemini")


def test_summarize_text(llm_provider):
    text = "This is a sample input text."
    summary = llm_provider.summarize_text(text)
    assert summary is not None
    assert isinstance(summary, str)
    assert len(summary) > 10  # Check that the summary is a reasonable length
