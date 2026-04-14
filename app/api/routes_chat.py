from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    try:
        answer = await usecase.ask(
            user_id=user_id,
            prompt=body.prompt,
            system=body.system,
            max_history=body.max_history,
            temperature=body.temperature,
        )
    except ExternalServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=exc.detail
        )
    return ChatResponse(answer=answer)


@router.get("/history")
async def history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    messages = await usecase.get_history(user_id)
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    await usecase.clear_history(user_id)
