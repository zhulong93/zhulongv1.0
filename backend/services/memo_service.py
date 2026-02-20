"""烛龙 - 备忘录服务"""
from datetime import datetime
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import MemoORM
from models import MemoItem


async def create_memo(
    session: AsyncSession,
    title: str,
    content: str = "",
    reminder_at: Optional[datetime] = None
) -> MemoItem:
    """创建备忘录"""
    memo = MemoORM(
        title=title,
        content=content,
        reminder_at=reminder_at,
    )
    session.add(memo)
    await session.commit()
    await session.refresh(memo)
    return MemoItem(
        id=memo.id,
        title=memo.title,
        content=memo.content or "",
        reminder_at=memo.reminder_at,
        is_completed=memo.is_completed,
        created_at=memo.created_at,
    )


async def list_memos(
    session: AsyncSession,
    include_completed: bool = False,
    limit: int = 50
) -> list[MemoItem]:
    """获取备忘录列表"""
    q = select(MemoORM).order_by(MemoORM.created_at.desc())
    if not include_completed:
        q = q.where(MemoORM.is_completed == False)
    q = q.limit(limit)
    result = await session.execute(q)
    rows = result.scalars().all()
    return [
        MemoItem(
            id=r.id,
            title=r.title,
            content=r.content or "",
            reminder_at=r.reminder_at,
            is_completed=r.is_completed,
            created_at=r.created_at,
        )
        for r in rows
    ]


async def get_pending_reminders(session: AsyncSession) -> list[MemoItem]:
    """获取待提醒的备忘录 (reminder_at <= now)"""
    now = datetime.utcnow()
    result = await session.execute(
        select(MemoORM).where(
            and_(
                MemoORM.reminder_at != None,
                MemoORM.reminder_at <= now,
                MemoORM.is_completed == False,
            )
        ).order_by(MemoORM.reminder_at)
    )
    rows = result.scalars().all()
    return [
        MemoItem(
            id=r.id,
            title=r.title,
            content=r.content or "",
            reminder_at=r.reminder_at,
            is_completed=r.is_completed,
            created_at=r.created_at,
        )
        for r in rows
    ]


async def complete_memo(session: AsyncSession, memo_id: int) -> bool:
    """标记完成"""
    result = await session.execute(select(MemoORM).where(MemoORM.id == memo_id))
    memo = result.scalar_one_or_none()
    if not memo:
        return False
    memo.is_completed = True
    await session.commit()
    return True


async def delete_memo(session: AsyncSession, memo_id: int) -> bool:
    """删除备忘录"""
    result = await session.execute(select(MemoORM).where(MemoORM.id == memo_id))
    memo = result.scalar_one_or_none()
    if not memo:
        return False
    await session.delete(memo)
    await session.commit()
    return True
