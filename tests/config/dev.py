"""开发环境配置"""
from .settings import BaseConfig


class DevConfig(BaseConfig):
    """开发环境配置"""
    env: str = "dev"
    base_url: str = "http://localhost:8080"
    db_host: str = "localhost"
    db_name: str = "dev_db"
