"""生产环境配置"""
from .settings import BaseConfig


class ProdConfig(BaseConfig):
    """生产环境配置（只读操作）"""
    env: str = "prod"
    base_url: str = "https://api.example.com"
    db_host: str = "prod-db.example.com"
    db_name: str = "prod_db"
