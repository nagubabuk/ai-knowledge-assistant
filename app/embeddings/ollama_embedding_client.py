"""
Ollama embedding client.

Responsible for generating vector embeddings using
an Ollama embedding model.

This client does not:
- Store vectors
- Search vectors
- Perform RAG
- Handle HTTP requests
"""

import logging 
from ollama import embed
from app.config import settings

logger =logging.getLogger(__name__)

class OllamaEmbeddingClient:
    def generate_embedding(self, text:str,) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty")
        logger.info(
            "Generating embedding using model '%s'",
            settings.OLLAMA_EMBEDDING_MODEL
        )

        response = embed(
            model=settings.OLLAMA_EMBEDDING_MODEL,
            input= text
        )

        embedding = response.embeddings[0]

        logger.info("Generated embedding with %d dimensions",len(embedding))

        return embedding
