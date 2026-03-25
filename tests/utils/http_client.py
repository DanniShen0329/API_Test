"""HTTP客户端封装"""
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

logger = logging.getLogger(__name__)


class HttpClient:
    """HTTP请求客户端，支持重试机制"""

    def __init__(self, base_url: str, timeout: int = 30, retry_times: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.retry_times = retry_times
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        logger.info(f"初始化HTTP客户端: base_url={base_url}, timeout={timeout}, retry_times={retry_times}")

    def get(self, path: str, **kwargs):
        """发送GET请求"""
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        """发送POST请求"""
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        """发送PUT请求"""
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        """发送DELETE请求"""
        return self._request("DELETE", path, **kwargs)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        reraise=True
    )
    def _request(self, method: str, path: str, **kwargs):
        """发送HTTP请求（带重试机制）"""
        url = f"{self.base_url}{path}"
        
        # 设置默认超时
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        
        logger.debug(f"发送 {method} 请求: {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            logger.debug(f"请求成功: {response.status_code}")
            return response
        except requests.Timeout as e:
            logger.error(f"请求超时: {url}")
            raise
        except requests.ConnectionError as e:
            logger.error(f"连接错误: {url}")
            raise
        except requests.HTTPError as e:
            logger.error(f"HTTP错误: {response.status_code} - {response.text}")
            raise

    def close(self):
        """关闭session"""
        self.session.close()
        logger.info("HTTP客户端已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
