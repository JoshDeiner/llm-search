import ollama  # Assuming you've installed the Ollama Python client


class OllamaLLM:
    _instance = None

    def __init__(self, model_name="llama3.2:latest"):
        """Private initializer to prevent direct instantiation."""
        if OllamaLLM._instance is None:
            self._model_name = model_name  # Private attribute for model name
            self.client = ollama  # Set up client as an instance attribute
            OllamaLLM._instance = self

    @classmethod
    def get_instance(cls):
        """Method to get the singleton instance of OllamaConfig."""
        if cls._instance is None:
            cls()  # Instantiate if it hasn't been created yet
        return cls._instance

    def generate_response(self, prompt):
        """Method to generate a response from the Ollama model."""
        return self.client.generate(model=self._model_name, prompt=prompt)

    def generate_streaming_response(self, prompt):
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

    # Generate a streaming response
    # print("Streaming Response:")
    # for line in ollama_llm.generate_streaming_response("Why is the sky blue?"):
    #     print(line)
