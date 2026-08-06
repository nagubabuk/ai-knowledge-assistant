import logging
from ollama import ResponseError, chat
from app.config import settings
from app.config import settings
from app.core.exceptions import AIProviderException
logger = logging.getLogger(__name__)

class OllamaClient:

    def generate(
        self,
        model: str,
        messages: list
    ) -> str:
        try:
            logger.info("Sending request to Ollama model %s", model)
            response = chat(
                model=model,
                messages=messages
            )
            logger.info("Received response from Ollama")
            return response.message.content
        except ResponseError as ex:
            logger.exception("Ollama returned an error.")

            raise AIProviderException(
                "Unable to generate AI response."
            ) from ex