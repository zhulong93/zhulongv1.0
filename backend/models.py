"""烛龙 - 数据模型"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MessagePriority(str, Enum):
    """微信消息优先级"""
    URGENT = "urgent"      # 紧急 - 马上处理
    NORMAL = "normal"      # 一般 - 1小时内
    ROUTINE = "routine"    # 常规 - 当天处理


class ContentType(str, Enum):
    """内容类型"""
    NEWS = "news"
    ARTICLE = "article"
    VIDEO = "video"


# === 信息提炼 ===
class ContentItem(BaseModel):
    """推送内容项"""
    id: Optional[int] = None
    title: str
    url: str
    source: str = ""
    summary: str = ""
    content_type: ContentType = ContentType.NEWS
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    relevance_score: float = 0.0  # 相关性分数


class ContentFeedback(BaseModel):
    """内容反馈 (0-5档)"""
    content_id: int
    score: int = Field(ge=0, le=5)
    comment: Optional[str] = None


# === 微信消息过滤 ===
class WeChatMessage(BaseModel):
    """微信消息"""
    id: Optional[int] = None
    sender: str
    content: str
    priority: MessagePriority = MessagePriority.ROUTINE
    received_at: Optional[datetime] = None
    is_read: bool = False


# === 备忘录 ===
class MemoItem(BaseModel):
    """备忘录项"""
    id: Optional[int] = None
    title: str
    content: str = ""
    reminder_at: Optional[datetime] = None
    is_completed: bool = False
    created_at: Optional[datetime] = None


# === 用户输入 ===
class UserInput(BaseModel):
    """用户输入 (语音转文字或直接文字)"""
    text: str
    input_type: str = "text"  # text | voice
