from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user_id: int, role: str, content: str) -> ChatMessage:
        msg = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(msg)
        await self._session.commit()
        await self._session.refresh(msg)
        return msg

    async def get_last_n(self, user_id: int, n: int) -> list[ChatMessage]:
        subq = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(n)
            .subquery()
        )
        result = await self._session.execute(
            select(ChatMessage)
            .join(subq, ChatMessage.id == subq.c.id)
            .order_by(ChatMessage.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_all(self, user_id: int) -> list[ChatMessage]:
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.asc())
        )
        return list(result.scalars().all())

    async def delete_all(self, user_id: int) -> None:
        await self._session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self._session.commit()
