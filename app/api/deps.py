from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


def get_user_repo(session: Annotated[AsyncSession, Depends(get_session)]) -> UserRepository:
    return UserRepository(session)


def get_msg_repo(session: Annotated[AsyncSession, Depends(get_session)]) -> ChatMessageRepository:
    return ChatMessageRepository(session)


def get_auth_usecase(user_repo: Annotated[UserRepository, Depends(get_user_repo)]) -> AuthUseCase:
    return AuthUseCase(user_repo)


def get_chat_usecase(
    msg_repo: Annotated[ChatMessageRepository, Depends(get_msg_repo)],
) -> ChatUseCase:
    return ChatUseCase(msg_repo=msg_repo, llm_client=OpenRouterClient())


def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)
