"""烛龙 - 信息提炼服务"""
from datetime import datetime
from typing import Optional
import httpx
import feedparser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import ContentORM, FeedbackORM, KeywordWeightORM
from models import ContentItem, ContentType
from config import get_settings


# 默认信息源 RSS (科技、商业、创业相关)
DEFAULT_FEEDS = [
    "https://www.36kr.com/feed",
    "https://rss.sina.com.cn/tech/roll.xml",
    "https://feedx.net/rss/ifanr.xml",
    "https://sspai.com/feed",
]


async def fetch_feeds() -> list[dict]:
    """从RSS源抓取内容"""
    items = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for feed_url in DEFAULT_FEEDS:
            try:
                resp = await client.get(feed_url)
                if resp.status_code == 200:
                    feed = feedparser.parse(resp.text)
                    for entry in feed.entries[:5]:
                        items.append({
                            "title": entry.get("title", ""),
                            "url": entry.get("link", ""),
                            "source": feed.feed.get("title", "未知"),
                            "summary": entry.get("summary", entry.get("description", ""))[:300],
                            "published": entry.get("published_parsed"),
                        })
            except Exception:
                continue
    return items


def calc_relevance(title: str, summary: str, keywords: list[str], weights: dict) -> float:
    """计算内容与用户兴趣的相关性分数"""
    text = (title + " " + summary).lower()
    score = 0.0
    for kw in keywords:
        weight = weights.get(kw.lower(), 1.0)
        if kw.lower() in text:
            score += weight
    return min(score, 10.0)


async def get_keyword_weights(session: AsyncSession) -> dict[str, float]:
    """获取关键词权重"""
    result = await session.execute(select(KeywordWeightORM))
    rows = result.scalars().all()
    return {r.keyword: r.weight for r in rows}


async def refine_and_rank(
    session: AsyncSession,
    limit: int = 10
) -> list[ContentItem]:
    """
    信息提炼：抓取、打分、排序、取TopN
    """
    settings = get_settings()
    keywords = settings.interest_keywords
    weights = await get_keyword_weights(session)
    
    raw_items = await fetch_feeds()
    scored = []
    for item in raw_items:
        score = calc_relevance(
            item["title"], item["summary"],
            keywords, weights
        )
        if score > 0 or len(scored) < limit * 2:  # 至少保留一些
            scored.append((score, item))
    
    # 按分数排序
    scored.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for score, item in scored[:limit]:
        published = None
        if item.get("published"):
            try:
                published = datetime(*item["published"][:6])
            except (TypeError, IndexError):
                pass
        
        content = ContentORM(
            title=item["title"],
            url=item["url"],
            source=item.get("source", ""),
            summary=item.get("summary", ""),
            content_type="news",
            published_at=published,
            relevance_score=score,
        )
        session.add(content)
        await session.flush()
        results.append(ContentItem(
            id=content.id,
            title=content.title,
            url=content.url,
            source=content.source,
            summary=content.summary,
            content_type=ContentType.NEWS,
            published_at=published,
            relevance_score=score,
        ))
    
    await session.commit()
    return results


async def record_feedback(
    session: AsyncSession,
    content_id: int,
    score: int,
    comment: Optional[str] = None
) -> None:
    """记录反馈，用于学习优化"""
    fb = FeedbackORM(content_id=content_id, score=score, comment=comment)
    session.add(fb)
    await session.commit()
    
    # 简单学习：根据高分反馈提取关键词并增加权重
    if score >= 4:
        result = await session.execute(
            select(ContentORM).where(ContentORM.id == content_id)
        )
        content = result.scalar_one_or_none()
        if content:
            settings = get_settings()
            for kw in settings.interest_keywords:
                if kw.lower() in (content.title + content.summary).lower():
                    # 更新或插入权重
                    r = await session.execute(
                        select(KeywordWeightORM).where(
                            KeywordWeightORM.keyword == kw.lower()
                        )
                    )
                    row = r.scalar_one_or_none()
                    if row:
                        row.weight = min(row.weight + 0.1, 3.0)
                    else:
                        session.add(KeywordWeightORM(keyword=kw.lower(), weight=1.2))
            await session.commit()
