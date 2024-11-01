# services/result_processing_service.py

import requests

class ResultProcessingService:
    def __init__(self, llm_core_plus_url: str):
        self.llm_core_plus_url = llm_core_plus_url

    def process_results(self, search_results: list) -> dict:
        """Processes results by summarizing and validating them."""
        response = requests.post(self.llm_core_plus_url, json={"results": search_results})
        response.raise_for_status()
        return response.json()
