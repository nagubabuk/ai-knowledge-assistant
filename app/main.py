from fastapi import FastAPI
from app.api.routes import router
from fastapi.responses import JSONResponse
from app.core.exceptions import AIProviderException
from app.core.logger import configure_logging

app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0"
)
configure_logging()

@app.exception_handler(AIProviderException)
async def ai_provider_exception_handler(
    request: Request,
    exc: AIProviderException,
):
    return JSONResponse(
        status_code=503,
        content={
            "message": exc.message
        },
    )

app.include_router(router)