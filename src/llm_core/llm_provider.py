# llm_core/llm_provider.py

import os

from src.llm_core.gemini_llm import GeminiLLM
from src.llm_core.llama_llm import OllamaLLM


# type?
def LLMProvider(model_name: str = "gemini") -> GeminiLLM:
    """Provides an instance of the specified LLM based on model_name."""
    if model_name.lower() == "gemini":
        return GeminiLLM.get_instance()
    elif model_name.lower() == "ollama":
        return OllamaLLM.get_instance()
    else:
        raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'")
