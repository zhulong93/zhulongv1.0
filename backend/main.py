"""烛龙 - API 主入口"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from database import init_db, get_session_factory
from pydantic import BaseModel
from models import (
    ContentFeedback, UserInput, MessagePriority
)
from services import (
    refine_and_rank, record_feedback,
    create_memo, list_memos, get_pending_reminders, complete_memo, delete_memo,
    import_message, list_messages, mark_read,
)

# 全局引擎和会话
_engine = None
_session_factory = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _engine, _session_factory
    _engine = await init_db()
    _session_factory = get_session_factory(_engine)
    yield
    if _engine:
        await _engine.dispose()


app = FastAPI(
    title="烛龙",
    description="AI数字分身 - 蒋延春",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_session():
    async with _session_factory() as session:
        yield session


# === 用户底层逻辑 ===
@app.get("/api/user/profile")
async def get_user_profile():
    """获取用户底层逻辑"""
    s = get_settings()
    return {
        "identity": s.user_identity,
        "transcendent": s.user_transcendent,
        "worldly": s.user_worldly,
    }


# === 信息提炼 ===
@app.get("/api/contents")
async def get_contents(session=Depends(get_session)):
    """获取今日推送内容 (若今日尚未生成则先生成)"""
    items = await refine_and_rank(session, limit=get_settings().daily_push_count)
    return [i.model_dump(mode="json") for i in items]


@app.post("/api/contents/{content_id}/feedback")
async def submit_feedback(content_id: int, fb: ContentFeedback, session=Depends(get_session)):
    """提交内容反馈 0-5 分"""
    await record_feedback(session, content_id, fb.score, fb.comment)
    return {"ok": True}


# === 备忘录 ===
@app.get("/api/memos")
async def get_memos(include_completed: bool = False, session=Depends(get_session)):
    """获取备忘录列表"""
    items = await list_memos(session, include_completed=include_completed)
    return [i.model_dump(mode="json") for i in items]


@app.get("/api/memos/reminders")
async def get_reminders(session=Depends(get_session)):
    """获取待提醒项 (提醒模式)"""
    items = await get_pending_reminders(session)
    return [i.model_dump(mode="json") for i in items]


@app.post("/api/memos/{memo_id}/complete")
async def complete_memo_api(memo_id: int, session=Depends(get_session)):
    """标记备忘录完成"""
    ok = await complete_memo(session, memo_id)
    if not ok:
        raise HTTPException(404, "备忘录不存在")
    return {"ok": True}


@app.delete("/api/memos/{memo_id}")
async def delete_memo_api(memo_id: int, session=Depends(get_session)):
    """删除备忘录"""
    ok = await delete_memo(session, memo_id)
    if not ok:
        raise HTTPException(404, "备忘录不存在")
    return {"ok": True}


# === 微信消息过滤 ===
@app.get("/api/wechat/messages")
async def get_wechat_messages(
    priority: str | None = None,
    unread_only: bool = False,
    session=Depends(get_session)
):
    """获取微信消息列表"""
    p = MessagePriority(priority) if priority else None
    items = await list_messages(session, priority=p, unread_only=unread_only)
    return [i.model_dump(mode="json") for i in items]


class MemoCreate(BaseModel):
    title: str
    content: str = ""
    reminder_at: datetime | None = None


class WeChatMessageCreate(BaseModel):
    sender: str
    content: str
    priority: str | None = None


@app.post("/api/memos")
async def add_memo(body: MemoCreate, session=Depends(get_session)):
    """创建备忘录"""
    item = await create_memo(
        session, body.title, body.content, body.reminder_at
    )
    return item.model_dump(mode="json")


@app.post("/api/wechat/messages")
async def add_wechat_message(
    body: WeChatMessageCreate,
    session=Depends(get_session)
):
    """导入微信消息 (供第三方工具调用)"""
    p = MessagePriority(body.priority) if body.priority else None
    item = await import_message(session, body.sender, body.content, p)
    return item.model_dump(mode="json")


@app.post("/api/wechat/messages/{msg_id}/read")
async def mark_message_read(msg_id: int, session=Depends(get_session)):
    """标记消息已读"""
    ok = await mark_read(session, msg_id)
    if not ok:
        raise HTTPException(404, "消息不存在")
    return {"ok": True}


# === 自然语言输入 (预留) ===
@app.post("/api/input")
async def handle_user_input(input_data: UserInput, session=Depends(get_session)):
    """
    处理用户语音/文字输入
    后续可接入 NLP 解析意图，分发到各模块
    """
    text = input_data.text.strip().lower()
    # 简单意图识别示例
    if "备忘" in text or "记住" in text or "记录" in text:
        return {"intent": "memo", "hint": "请提供备忘录标题和内容"}
    if "今日推送" in text or "今日内容" in text:
        return {"intent": "contents", "hint": "正在获取今日推送"}
    if "微信" in text or "消息" in text:
        return {"intent": "wechat", "hint": "正在获取消息列表"}
    return {"intent": "unknown", "text": input_data.text}


@app.get("/")
async def root():
    return {
        "name": "烛龙",
        "version": "1.0.0",
        "message": "AI数字分身 API",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
