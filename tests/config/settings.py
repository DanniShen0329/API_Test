"""环境配置基类"""
from pydantic_settings import BaseSettings
from typing import Optional


class BaseConfig(BaseSettings):
    """基础配置类"""
    env: str = "test"
    base_url: str = ""
    timeout: int = 30
    retry_times: int = 3
    
    # API认证
    api_sid: Optional[str] = None
    
    # 可选的数据库配置
    db_host: Optional[str] = None
    db_name: Optional[str] = None
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # 忽略未定义的字段
    }
