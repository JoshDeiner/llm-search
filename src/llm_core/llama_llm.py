import ollama

from typing import Optional
from typing import Generator
from typing import Any



class OllamaLLM:
    _instance: Optional["OllamaLLM"] = None

    def __init__(self, model_name: str = "llama3.2:latest") -> None:
        """Private initializer to prevent direct instantiation."""
        if OllamaLLM._instance is None:
            self._model_name: str = model_name  # Private attribute for model name
            self.client: Any = ollama  # Set up client as an instance attribute
            OllamaLLM._instance = self

    @classmethod
    def get_instance(cls) -> "OllamaLLM":
        """Method to get the singleton instance of OllamaLLM."""
        if cls._instance is None:
            cls()  # Instantiate if it hasn't been created yet
        return cls._instance

    def generate_response(self, prompt: str) -> Optional[str]:
        """Method to generate a response from the Ollama model."""
        return self.client.generate(model=self._model_name, prompt=prompt)

    def generate_streaming_response(self, prompt: str) -> Generator[str, None, None]:
        """Generator function to stream the model output."""
        for output in self.client.generate(
            model=self._model_name, prompt=prompt, stream=True
        ):
            yield output


if __name__ == "__main__":
    ollama_llm = OllamaLLM.get_instance()

    # Generate a full response
    response = ollama_llm.generate_response("Why is the sky blue?")
    if response:
        print("Full Response:", response)
    else:
        print("No response received")
