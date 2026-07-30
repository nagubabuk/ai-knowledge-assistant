from fastapi import APIRouter
from fastapi import Depends

from app.dependencies import get_llm_service
from app.models import ChatRequest, ChatResponse
from app.services.llm_service import LLMService

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


@router.get("/greet")
def greetings():
    return {
        'status': "greetings",
        'message': "Hello this is AI Assistant"
    }