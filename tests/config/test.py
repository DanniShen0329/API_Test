"""测试环境配置"""
from .settings import BaseConfig


class TestConfig(BaseConfig):
    """测试环境配置"""
    env: str = "test"
    base_url: str = "http://172.17.12.107:9909"
    db_host: str = "172.17.12.217:1521"
    db_name: str = "cdlddb"
