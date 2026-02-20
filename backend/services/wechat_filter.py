"""烛龙 - 微信消息过滤服务

注意：微信个人版暂无官方开放API，本模块提供：
1. 模拟消息导入与分类（用于演示/测试）
2. 分类规则引擎（紧急/一般/常规）
3. 与第三方工具（如 itchat、WeChatFerry 等）对接的接口预留
"""
import re
from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import WeChatMessageORM
from models import WeChatMessage, MessagePriority


# 紧急关键词
URGENT_KEYWORDS = [
    "紧急", "立刻", "马上", "立刻", "urgent", "asap",
    "客户", "订单", "合同", "故障", "宕机", "事故"
]

# 一般关键词 (1小时内)
NORMAL_KEYWORDS = [
    "今天", "待办", "会议", "回复", "确认", "审批"
]


def classify_message(content: str, sender: str = "") -> MessagePriority:
    """
    根据内容和发送者分类消息优先级
    """
    text = (content + " " + sender).lower()
    for kw in URGENT_KEYWORDS:
        if kw in text:
            return MessagePriority.URGENT
    for kw in NORMAL_KEYWORDS:
        if kw in text:
            return MessagePriority.NORMAL
    return MessagePriority.ROUTINE


async def import_message(
    session: AsyncSession,
    sender: str,
    content: str,
    priority: Optional[MessagePriority] = None
) -> WeChatMessage:
    """
    导入一条微信消息并自动分类
    （实际场景中由第三方工具调用此接口）
    """
    if priority is None:
        priority = classify_message(content, sender)
    
    msg = WeChatMessageORM(
        sender=sender,
        content=content,
        priority=priority.value,
    )
    session.add(msg)
    await session.commit()
    await session.refresh(msg)
    return WeChatMessage(
        id=msg.id,
        sender=msg.sender,
        content=msg.content,
        priority=MessagePriority(msg.priority),
        received_at=msg.received_at,
        is_read=msg.is_read,
    )


async def list_messages(
    session: AsyncSession,
    priority: Optional[MessagePriority] = None,
    unread_only: bool = False,
    limit: int = 50
) -> list[WeChatMessage]:
    """获取消息列表"""
    q = select(WeChatMessageORM).order_by(
        # 紧急优先，然后按时间
        WeChatMessageORM.received_at.desc()
    ).limit(limit)
    if priority:
        q = q.where(WeChatMessageORM.priority == priority.value)
    if unread_only:
        q = q.where(WeChatMessageORM.is_read == False)
    result = await session.execute(q)
    rows = result.scalars().all()
    return [
        WeChatMessage(
            id=r.id,
            sender=r.sender,
            content=r.content,
            priority=MessagePriority(r.priority),
            received_at=r.received_at,
            is_read=r.is_read,
        )
        for r in rows
    ]


async def mark_read(session: AsyncSession, msg_id: int) -> bool:
    """标记已读"""
    result = await session.execute(
        select(WeChatMessageORM).where(WeChatMessageORM.id == msg_id)
    )
    msg = result.scalar_one_or_none()
    if not msg:
        return False
    msg.is_read = True
    await session.commit()
    return True
