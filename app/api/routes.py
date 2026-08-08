from fastapi import APIRouter
from fastapi import Depends

from app.dependencies import get_llm_service
from app.models import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from fastapi.responses import StreamingResponse

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
    request:ChatRequest,
    llm_service:LLMService = Depends(get_llm_service)
):
    return StreamingResponse(
        llm_service.generate_stream_response(
            request.message
        ),
        media_type="text/plain"
    )

@router.get("/greet")
def greetings():
    return {
        'status': "greetings",
        'message': "Hello this is AI Assistant"
    }