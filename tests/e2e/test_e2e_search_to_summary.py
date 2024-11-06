# tests/e2e/test_e2e_search_to_summary.py
import pytest
import logging
from src.user_service.factory import get_user_service
from src.core_pipeline.stages.data_processing import process_results
from src.core_pipeline.stages.summarization import summarize_results
from src.llm_core.llm_provider import LLMProvider


@pytest.fixture
def user_service():
    return get_user_service()


@pytest.fixture
def llm_provider():
    return LLMProvider(model_name="gemini")


def test_e2e_search_to_summary(user_service, llm_provider):
    search_term = "landmarks in Paris"

    # Step 1: Run search and validate results
    search_data = user_service.search(search_term)
    logging.debug(f"Search Data: {search_data}")

    assert "search_term" in search_data
    assert "web_results" in search_data
    assert "validation_results" in search_data

    # Step 2: Process results for summarization
    results_text = process_results(search_data["web_results"])
    logging.debug(f"Processed Results Text: {results_text}")
    assert results_text is not None
    assert "No results found" not in results_text

    # Step 3: Summarize the results
    summary = summarize_results(llm_provider, results_text)
    logging.debug(f"Generated Summary: {summary}")
    assert summary is not None
    assert "Summary could not be generated" not in summary

    # Step 4: Check summary relevance
    relevance_check_prompt = (
        f"Is this summary relevant for the search term '{search_term}'? "
        "The summary should mention popular places or landmarks in Paris. "
        "Respond with 'Yes' or 'No' only."
    )
    relevance_response = llm_provider.generate_text(
        f"{relevance_check_prompt}\n\nSummary:\n{summary}"
    )
    logging.debug(f"Relevance Response: {relevance_response}")

    # Final assertion based on model response or keyword fallback
    if "Yes" not in relevance_response:
        assert any(
            keyword in summary for keyword in ["Paris", "landmark", "popular"]
        ), "The summary did not meet relevance criteria, even with keyword fallback."
    else:
        assert (
            "Yes" in relevance_response
        ), "The summary did not meet relevance criteria for the search term."
