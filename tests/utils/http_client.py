"""HTTP客户端封装"""
import logging
import json
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

    def _log_request(self, method: str, url: str, headers: dict, json_data: dict = None):
        """记录请求信息"""
        logger.info(f"=" * 60)
        logger.info(f"[REQUEST] {method} {url}")
        logger.info(f"[REQUEST HEADERS] {json.dumps(dict(headers), indent=2, ensure_ascii=False)}")
        if json_data:
            logger.info(f"[REQUEST BODY] {json.dumps(json_data, indent=2, ensure_ascii=False)}")
        logger.info(f"=" * 60)

    def _log_response(self, response: requests.Response, elapsed_ms: float):
        """记录响应信息"""
        logger.info(f"-" * 60)
        logger.info(f"[RESPONSE] Status: {response.status_code} ({elapsed_ms:.2f}ms)")
        try:
            if response.text:
                resp_body = response.json()
                logger.info(f"[RESPONSE BODY] {json.dumps(resp_body, indent=2, ensure_ascii=False)}")
            else:
                logger.info(f"[RESPONSE BODY] (empty)")
        except ValueError:
            logger.info(f"[RESPONSE BODY] {response.text}")
        logger.info(f"-" * 60)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        reraise=True
    )
    def _request(self, method: str, path: str, **kwargs):
        """发送HTTP请求（带重试机制）"""
        import time
        
        url = f"{self.base_url}{path}"
        
        # 设置默认超时
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        
        # 获取请求体用于日志记录
        json_data = kwargs.get('json') or kwargs.get('data')
        headers = kwargs.get('headers', self.session.headers)
        
        # 记录请求
        self._log_request(method, url, headers, json_data)
        
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, **kwargs)
            elapsed_ms = (time.time() - start_time) * 1000
            
            # 记录响应
            self._log_response(response, elapsed_ms)
            
            response.raise_for_status()
            return response
        except requests.Timeout as e:
            logger.error(f"[ERROR] 请求超时: {url}")
            raise
        except requests.ConnectionError as e:
            logger.error(f"[ERROR] 连接错误: {url}")
            raise
        except requests.HTTPError as e:
            logger.error(f"[ERROR] HTTP错误: {response.status_code} - {response.text}")
            raise

    def close(self):
        """关闭session"""
        self.session.close()
        logger.info("HTTP客户端已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
