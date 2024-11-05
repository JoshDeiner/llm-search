# core_pipeline/main_pipeline.py

import logging
from core_pipeline.stages.search_execution import (
    fetch_web_results,
    validate_search_results,
)
from core_pipeline.stages.summarization import summarize_results
from llm_core.llm_provider import LLMProvider
from core_pipeline.stages.search_execution import retry_with_validation

from services.search_engine_client import SearchEngineClient
from user_service.user import User


def main_pipeline(user_service: User, search_term: str) -> None:
    """
    Main pipeline to fetch, validate, process, and summarize web search results.

    Parameters:
    - user_service: The service handling the search operation.
    - search_term: The search term to query.
    """
    # Initialize the LLM provider for summarization
    llm_provider = LLMProvider(model_name="gemini")

    # se_client = SearchEngineClient()

    # se_client.search("where is")

    # search_data = fetch_web_results(user_service, search_term)
    # print("web", search_data["web_results"])

    # search_results_validated = validate_search_results(search_data)

    # raw_search_data = retry_with_validation(validate_search_results, search_data)

    # print("yo", search_data)

    # Step 1: Fetch web results with retry mechanism
    raw_search_data = retry_with_validation(
        fetch_web_results, user_service, search_term
    )

    if raw_search_data is None:
        logging.error("Failed to fetch search results after retries.")
        return

    # Step 2: Validate and process the fetched results
    validated_results_text = validate_search_results(raw_search_data)

    if validated_results_text is None:
        logging.error("No valid results to process for summarization.")
        return

    # Step 3: Summarize the validated results
    summary = summarize_results(llm_provider, validated_results_text)
    if summary is None:
        logging.error("Summary generation failed.")
        return

    logging.info("Summary generation succeeded.")
    logging.info("Final Summary:")
    logging.info(summary)
