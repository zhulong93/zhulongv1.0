"""烛龙 - 数据库层"""
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import get_settings

Base = declarative_base()


class ContentORM(Base):
    """推送内容表"""
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)
    source = Column(String(200), default="")
    summary = Column(Text, default="")
    content_type = Column(String(20), default="news")
    published_at = Column(DateTime, nullable=True)
    relevance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class FeedbackORM(Base):
    """反馈表"""
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)  # 0-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MemoORM(Base):
    """备忘录表"""
    __tablename__ = "memos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    content = Column(Text, default="")
    reminder_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class WeChatMessageORM(Base):
    """微信消息表 (模拟/导入用)"""
    __tablename__ = "wechat_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default="routine")  # urgent, normal, routine
    received_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)


class KeywordWeightORM(Base):
    """关键词权重表 (用于学习优化)"""
    __tablename__ = "keyword_weights"
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(100), nullable=False, unique=True)
    weight = Column(Float, default=1.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 异步数据库引擎
def get_async_engine():
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=False
    )


async def init_db():
    """初始化数据库"""
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


def get_session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
