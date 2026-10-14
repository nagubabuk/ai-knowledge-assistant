from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "AI Knowledge Assistant"

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text:latest"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()