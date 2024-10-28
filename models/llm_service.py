import os
from gemini_llm import GeminiLLM
from ollama_llm import OllamaLLM


def llm_service(model_name="gemini"):
    """Returns an instance of the specified LLM based on model_name."""
    # llm_dict = {
    #     "gemini": GeminiLLM,
    #     "ollama": OllamaLLM
    # }
    # llm_class = llm_dict.get(model_name.lower(), "gemini")
    # llm_class.get_instance()

    if model_name.lower() == "gemini":
        return GeminiLLM.get_instance()
    elif model_name.lower() == "ollama":
        return OllamaLLM.get_instance()
    else:
        raise ValueError("Unsupported model name. Choose 'gemini' or 'ollama'.")


# Usage example
if __name__ == "__main__":
    # Choose model based on environment variable or explicit argument
    model_choice = os.getenv(
        "LLM_MODEL", "gemini"
    )  # Default to Gemini if no environment variable set
    llm = get_llm_service(model_choice)

    # Generate response
    response = llm.generate_response(
        "Explain how AI works" if model_choice == "gemini" else "Why is the sky blue?"
    )
    print("Response:", response)
