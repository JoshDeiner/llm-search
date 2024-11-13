# llm_core/llm_provider.py


from src.features.llm_core.gemini_llm import GeminiLLM
from src.features.llm_core.llama_llm import OllamaLLM
from src.features.llm_core.singleton import singleton

from typing import Union

def LLMProvider(model_name: str = "gemini") -> Union[GeminiLLM, OllamaLLM]:
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

    models = {
        "gemini": GeminiLLM,
        "ollama": OllamaLLM
    }

# mypy seems to have problem or is out of date
# shouldnt you says models.get(model_name) instead of models[model_name]?
    model = models.get(model_name, 0)
    if model:
        return singleton(model)
    else:
        raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'.")
    # if model_name in models:
    #     return singleton(models[model_name])
    # else:
    #     raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'.")

    # if (model_name == "gemini"):
    #     return singleton(GeminiLLM)
    # elif (model_name == "ollama"):
    #     return singleton(OllamaLLM)
    # else:
    #     raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'.")


# mypy seems to have problem or is out of date
    # match model_name:
    #     case "gemini":
    #         return singleton(GeminiLLM)
    #     case "ollama":
    #         return singleton(OllamaLLM)
    #     case _:
    #         raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'.")
