# llm_core/gemini_llm.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

from src.llm_core.llm_core import LLMCore

load_dotenv()  # Load environment variables


class GeminiLLM(LLMCore):
    _instance = None

    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        """Initialize the Gemini model with configuration from environment variables."""
        # Call the initializer of the parent class LLMCore
        super().__init__()  # This ensures any initialization in LLMCore is run

        if GeminiLLM._instance is None:
            GEMINI_KEY = os.getenv("GEMINI_KEY")
            self._model_name = model_name
            genai.configure(api_key=GEMINI_KEY)
            self.model = genai.GenerativeModel(self._model_name)
            GeminiLLM._instance = self
        else:
            raise Exception(
                "GeminiLLM instance already exists. Use get_instance() instead."
            )

    @classmethod
    def get_instance(cls) -> "GeminiLLM":
        """Singleton access method for the GeminiLLM class."""
        if cls._instance is None:
            cls._instance = GeminiLLM()
        return cls._instance

    @property
    def model_name(self):
        """Getter for the model name if access is needed."""
        return self._model_name
