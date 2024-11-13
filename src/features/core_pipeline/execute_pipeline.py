# core_pipeline/execute_pipeline.py

import logging
from typing import List
from src.shared.config.types import SearchResult
from src.features.core_pipeline.stages.search_execution import (
    fetch_web_results,
    validate_search_results,
)
from src.features.core_pipeline.stages.summarization import summarize_results
from src.features.core_pipeline.stages.document_service import DocumentPipeline
from src.features.llm_core.llm_provider import LLMProvider
from src.features.core_pipeline.stages.search_execution import retry_with_validation
from src.features.users.models.user import User


def extract_works_cited(results: List[SearchResult]) -> List[str]:
    works_cited = []
    for result in results:
        if isinstance(result, dict) and "title" in result:
            title = result["title"]
            link = result.get("link", "No Link") or "No Link"
            works_cited.append(f"{title}: {link}")
        else:
            logging.warning("Skipping invalid result entry: %s", result)
    print("Works Cited:", works_cited)
    return works_cited


def execute_pipeline(user_service: User, search_term: str) -> None:
    """
    Main pipeline to fetch, validate, process, and summarize web search results.

    Parameters:
    - user_service: The service handling the search operation.
    - search_term: The search term to query.
    """
    # Initialize the LLM provider for summarization
    llm_provider = LLMProvider(model_name="gemini")

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
    # add error handling for if summary is some form of incorrect of make summarize_results do it

    logging.info("Summary generation succeeded.")
    logging.info(f"Final Summary:\n{summary}")

    # Step 3.1: Extract works cited from all_results
    all_results = raw_search_data.get("all_results", [])
    works_cited = extract_works_cited(all_results)

    # Step 4: Write summary to document
    try:
        document_pipeline = DocumentPipeline(
            summary=summary,
            topic=search_term,
            file_type="md",
            works_cited=works_cited,
        )
        document_pipeline.save_to_file(
            file_name="pipeline_output", file_extension=".md"
        )
        logging.info("Document successfully saved.")
    except PermissionError:
        logging.error("Permission denied: Unable to save the document.")
    except IOError as e:
        logging.error(f"IOError occurred while saving the document: {e}")
    except Exception as e:
        logging.error("An unexpected error occurred in document saving.", exc_info=True)
