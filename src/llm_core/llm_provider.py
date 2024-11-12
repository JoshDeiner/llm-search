# llm_core/llm_provider.py


from src.llm_core.gemini_llm import GeminiLLM
from src.llm_core.llama_llm import OllamaLLM
from src.llm_core.singleton_util import get_instance


def LLMProvider(model_name: str = "gemini"):
    """
    Provides an instance of the specified LLM based on model_name.

    Args:
        model_name (str): The name of the LLM model to use.
                          Options are 'gemini' (default) or 'ollama'.

    Returns:
        An instance of the requested LLM class.

    Raises:
        ValueError: If the provided model_name is unsupported.
    """
    model_name = model_name.lower()

    match model_name:
        case "gemini":
            return get_instance(GeminiLLM)
        case "ollama":
            return get_instance(OllamaLLM)
        case _:
            raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'.")
