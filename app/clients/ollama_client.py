from ollama import chat
from app.config import settings


class OllamaClient:

    def generate(
        self,
        model: str,
        messages: list
    ) -> str:

        response = chat(
            model=model,
            messages=messages
        )

        return response.message.content