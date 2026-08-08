import logging
from ollama import chat
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
                messages=messages,
                stream=True
            )
            logger.info("Received response from Ollama")
            return response.message.content
        except Exception as ex:
            logger.exception("Unexpected error")

            raise AIProviderException(
                "Unable to generate AI response."
            ) from ex


    def generate_stream(
            self,
            model: str,
            message:list
    ):
        try:
            logger.info("streaming response from ollama model '%s'",model)
            stream = chat(
                model,
                messages=message,
                stream=True
            )

            for chunk in stream:
                content = chunk.message.content
                if content:
                    yield content
                

            logger.info("Streaming completed successfully.")

        except Exception as ex:
            logger.exception("streaming failed")

            raise AIProviderException(
                "Unable to stream api response"
            ) from ex
