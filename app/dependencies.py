from app.clients.ollama_client import OllamaClient
from app.services.llm_service import LLMService


def get_ollama_client() -> OllamaClient:
    return OllamaClient()


def get_llm_service() -> LLMService:
    client = get_ollama_client()
    return LLMService(client)