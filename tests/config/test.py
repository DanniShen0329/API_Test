"""测试环境配置"""
from .settings import BaseConfig


class TestConfig(BaseConfig):
    """测试环境配置"""
    env: str = "test"
    base_url: str = "http://xxxxx:9909"
    db_host: str = "xxxx:1521"
    db_name: str = "db"
