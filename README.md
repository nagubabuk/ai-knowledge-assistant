# AI Knowledge Assistant

A production-style AI chatbot built using FastAPI and Ollama.

## Features

- FastAPI REST API
- Local LLM integration using Ollama
- Prompt Builder architecture
- Dependency Injection
- Configuration management
- Layered architecture

## Tech Stack

- Python
- FastAPI
- Ollama
- Llama 3.2
- Pydantic

## Architecture Highlights

- Layered architecture (API → Service → Client)
- Dependency Injection using FastAPI
- Centralized configuration management
- Production-style logging
- Global exception handling
- Local LLM integration using Ollama

## Day 3 Enhancements

### Logging

- Centralized logging using Python's `logging` module.
- Module-specific loggers using `logging.getLogger(__name__)`.

### Exception Handling

- Custom `AIProviderException`.
- Global FastAPI exception handler.
- Clean HTTP responses for AI service failures.

### Architecture Improvements

- Prompt Builder
- Ollama Client abstraction
- Dependency Injection
- Configuration using `.env`
