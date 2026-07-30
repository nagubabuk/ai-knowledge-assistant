
from app.config import settings
from app.prompts.chat_prompt import ChatPromptBuilder
from app.clients.ollama_client import OllamaClient


class LLMService:

    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def generate_response(self, prompt: str):

        messages = ChatPromptBuilder.build(prompt)
        print('messages**',messages)
        print('settings', settings.OLLAMA_MODEL)
        return self.ollama_client.generate(
            settings.OLLAMA_MODEL,
            messages
        )