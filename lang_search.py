import pprint
import logging
import argparse
import os

from dotenv import load_dotenv
from llm_core.llm_provider import LLMProvider  # Import LLM provider
from user_service.factory import get_user_service
from requests.exceptions import RequestException  # Example of handling network errors

logging.basicConfig(filename="./logs/query.log", level=logging.INFO)


def validate_se_results(search_data):
    """
    Validate search engine (SE) results based on the search query.

    Parameters:
    search_data (dict): Dictionary containing search results and validation information.

    Returns:
    list: A list of validated search engine results, or all results as a fallback if none are validated.
    """
    web_results = search_data.get("web_results", [])
    se_validation_results = search_data.get("validation_results", [])

    # Log raw web results and validation results for debugging
    logging.info("Raw web search results:")
    logging.info(pprint.pformat(web_results))
    logging.info("Search engine validation results:")
    logging.info(pprint.pformat(se_validation_results))

    # Filter search engine validated results
    validated_se_results = [
        result
        for result, validation in zip(web_results, se_validation_results)
        if validation.get("is_valid", False)
    ]

    # If no results are validated by the search engine, use all results as fallback
    return validated_se_results if validated_se_results else web_results


def validate_summary(llm_core, summary, results_text):
    """
    Validate and score the generated summary based on the original search results.

    Parameters:
    llm_core (LLMProvider): The LLM provider instance.
    summary (str): The generated summary text.
    results_text (str): The concatenated search results text for comparison.

    Returns:
    dict: The validation outcome and information about the summary.
    """
    try:
        summary_validation_result = llm_core.validate_and_score_summary(
            summary, results_text
        )
    except Exception as e:
        logging.error(f"Error during summary validation: {e}")
        # Return a default failure response indicating a validation process error
        return {"is_valid": False, "reason": "Validation process encountered an error"}

    # Log validation results for the summary
    logging.info("Summary Validation Result:")
    logging.info(pprint.pformat(summary_validation_result))

    # Check and log based on validation results
    if summary_validation_result.get("is_valid"):
        logging.info("Summary is valid according to validation criteria.")
        logging.info("Final Summary:")
        logging.info(summary)
    else:
        logging.warning(
            f"Summary validation failed: {summary_validation_result.get('reason')}"
        )
        logging.info(
            f"Summary did not meet criteria. Final score: {summary_validation_result.get('score')}"
        )

        # Extra logging for debugging if failure patterns are noticed
        if summary_validation_result.get("score", 0) < 0.5:
            logging.critical(
                "Critical low score detected in validation. Investigate data or LLM performance."
            )

        logging.info("Final Summary (Unvalidated):")
        logging.info(summary)

    return summary_validation_result


def main(search_term: str):
    logging.info("Initializing search process")
    load_dotenv()

    user_service = get_user_service()
    llm_core = LLMProvider(model_name="gemini")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        logging.info(f"Attempt {attempt} of {max_retries}")

        try:
            # Run search process to get raw results and validation results
            search_data = user_service.search(search_term)
        except RequestException as e:
            logging.error(f"Network error during search attempt {attempt}: {e}")
            if attempt == max_retries:
                logging.error(
                    "Failed to retrieve search results after maximum retries."
                )
                return  # Exit if we’ve hit the max retries
            continue  # Retry on next loop iteration if not max attempts

        # Validate search engine results for summarization
        validated_se_results = validate_se_results(search_data)

        # Combine the validated search engine results for summarization
        results_text = "\n\n".join(validated_se_results)

        try:
            # Generate the summary
            summary = llm_core.summarize_text(results_text)
            logging.info("Generated Summary:")
            logging.info(summary)
        except Exception as e:
            logging.error(f"Error during summary generation on attempt {attempt}: {e}")
            if attempt == max_retries:
                logging.error("Failed to generate summary after maximum retries.")
                return  # Exit if we’ve hit the max retries
            continue  # Retry on next loop iteration if not max attempts

        # Validate the summary
        summary_validation_result = validate_summary(llm_core, summary, results_text)

        # Check if the summary validation passed
        if summary_validation_result.get("is_valid"):
            logging.info("Summary validation succeeded.")
            break
        elif attempt < max_retries:
            logging.warning(f"Validation failed on attempt {attempt}. Retrying...")
        else:
            logging.error("Validation failed after maximum retries.")


if __name__ == "__main__":
    # Parse CLI argument for the search term
    parser = argparse.ArgumentParser(description="Search with search_engine")
    parser.add_argument(
        "search_term",
        nargs="?",
        default="what do the experts say about the yankees struggles vs the dodgers",
        help="The search term to query search_engine",
    )

    args = parser.parse_args()

    # Execute main function with the provided search term
    main(args.search_term)
    logging.info("Search process completed.")
