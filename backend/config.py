"""烛龙 - 配置管理"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    app_name: str = "烛龙"
    app_version: str = "1.0.0"
    
    # 数据库 (Railway 等云平台可通过 DATABASE_URL 注入)
    database_url: str = "sqlite+aiosqlite:///./zhulong.db"
    
    # 每日推送数量
    daily_push_count: int = 10
    
    # 用户底层逻辑 - 蒋延春
    user_identity: str = "捷视飞通公司(ifreecomm)创始人、董事长、CEO；创业者"
    user_transcendent: str = "佛陀的追随者，个人终极使命：成为觉悟者(明心见性、立地成佛)，行菩萨道"
    user_worldly: str = "入世修行；创造价值、创造财富；方向：科技+商业；无为法：无为无不为"
    
    # 兴趣关键词 (用于信息筛选，可根据反馈动态调整)
    interest_keywords: list[str] = [
        "科技创业", "企业管理", "人工智能", "佛教", "修行",
        "商业", "捷视飞通", "视讯", "智慧教育", "创业"
    ]
    
    class Config:
        env_file = ".env"
        extra = "ignore"


def _get_database_url() -> str:
    """优先使用 DATABASE_URL 环境变量（Railway/Heroku 等）"""
    url = os.environ.get("DATABASE_URL")
    if url:
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url
    return "sqlite+aiosqlite:///./zhulong.db"


@lru_cache()
def get_settings() -> Settings:
    s = Settings()
    object.__setattr__(s, "database_url", _get_database_url())
    return s
