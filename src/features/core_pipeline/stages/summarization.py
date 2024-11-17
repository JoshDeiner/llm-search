import logging
from src.features.llm_core.llm_provider import LLMProvider


def summarize_results(llm_provider: LLMProvider, results_text: str) -> str:
    """
    Summarizes the search results text using the LLM core.

    Parameters:
    llm_core (LLMProvider): An instance of the LLM provider used for generating summaries.
    results_text (str): Concatenated search results text to be summarized.

    Returns:
    str: A summary of the search results.
    """
    summary: str

    try:
        summary = llm_provider.summarize_text(results_text)
        logging.info("Summary generated successfully.")
        logging.info("Summary Content:")
        logging.info(summary)
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
    finally:
        return summary
