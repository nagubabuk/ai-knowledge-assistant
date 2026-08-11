from fastapi import APIRouter
from fastapi import Depends
import logging

from app.dependencies import get_llm_service
from app.models import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.core.sse import format_sse_event
from app.core.exceptions import AIProviderException
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter()



@router.get("/health")
def health():
    return {
        "status": "UP",
        "message": "AI Service is running"
    }


@router.post("/chat")
def chat(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    response = llm_service.generate_response(request.message)

    return ChatResponse(
        reply=response
    )

@router.post("/chat/stream")
def chat_stream(
    request: ChatRequest,
    llm_service: LLMService = Depends(
        get_llm_service
    ),
):
    def event_generator():
        try:
            for chunk in (
                llm_service.generate_stream_response(
                    request.message
                )
            ):
                yield format_sse_event(
                    data=chunk,
                    event="message",
                )

            yield format_sse_event(
                data="completed",
                event="done",
            )

        except AIProviderException as ex:
            logger.exception(
                "Streaming AI request failed."
            )

            yield format_sse_event(
                data=str(ex),
                event="error",
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
@router.get("/greet")
def greetings():
    return {
        'status': "greetings",
        'message': "Hello this is AI Assistant"
    }