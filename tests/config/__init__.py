import os
from .dev import DevConfig
from .test import TestConfig
from .prod import ProdConfig

CONFIG_MAP = {
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig,
}


def get_config():
    """获取当前环境配置"""
    env = os.getenv("TEST_ENV", "test")
    return CONFIG_MAP.get(env, TestConfig)()
