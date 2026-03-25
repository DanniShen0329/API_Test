"""全局fixture配置"""
import pytest
import logging

from tests.config import get_config
from tests.data import price_group_data
from tests.utils.http_client import HttpClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config():
    """全局配置fixture"""
    return get_config()


@pytest.fixture(scope="session")
def api_client(config):
    """API客户端fixture"""
    client = HttpClient(
        base_url=config.base_url,
        timeout=config.timeout,
        retry_times=config.retry_times
    )
    yield client
    client.close()


@pytest.fixture
def valid_price_group_requests():
    """有效的价格组请求数据"""
    return price_group_data["valid_requests"]


@pytest.fixture
def invalid_price_group_requests():
    """无效的价格组请求数据"""
    return price_group_data["invalid_requests"]


@pytest.fixture
def edge_case_price_group_requests():
    """边界情况价格组请求数据"""
    return price_group_data["edge_cases"]


@pytest.fixture
def auth_headers():
    """认证请求头"""
    # 从环境变量或配置中获取sid
    import os
    sid = os.getenv("API_SID", "test-sid")
    return {"sid": sid}
