"""断言工具封装"""
import re
from typing import Any, Dict, List, Optional


class APIAssertions:
    """API测试断言工具类"""

    @staticmethod
    def assert_status_code(response, expected_code: int):
        """断言状态码"""
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"期望状态码 {expected_code}, 实际状态码 {actual_code}"

    @staticmethod
    def assert_json_schema(response, required_fields: List[str]):
        """断言JSON响应包含必填字段"""
        data = response.json()
        for field in required_fields:
            assert field in data, f"响应中缺少必填字段: {field}"

    @staticmethod
    def assert_field_value(response, field: str, expected_value: Any):
        """断言字段值"""
        data = response.json()
        actual_value = data.get(field)
        assert actual_value == expected_value, \
            f"字段 {field} 期望值 {expected_value}, 实际值 {actual_value}"

    @staticmethod
    def assert_field_exists(response, field: str):
        """断言字段存在"""
        data = response.json()
        assert field in data, f"响应中缺少字段: {field}"

    @staticmethod
    def assert_field_not_none(response, field: str):
        """断言字段不为空"""
        data = response.json()
        value = data.get(field)
        assert value is not None, f"字段 {field} 不能为空"

    @staticmethod
    def assert_field_match_regex(response, field: str, pattern: str):
        """断言字段值匹配正则表达式"""
        data = response.json()
        value = data.get(field, "")
        assert re.match(pattern, str(value)), \
            f"字段 {field} 值 {value} 不匹配模式 {pattern}"

    @staticmethod
    def assert_response_time(response, max_time_ms: float):
        """断言响应时间"""
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < max_time_ms, \
            f"响应时间 {elapsed_ms:.2f}ms 超过阈值 {max_time_ms}ms"

    @staticmethod
    def assert_header_exists(response, header_name: str):
        """断言响应头存在"""
        assert header_name in response.headers, \
            f"响应头中缺少 {header_name}"

    @staticmethod
    def assert_error_message(response, expected_message: str):
        """断言错误消息"""
        data = response.json()
        error_msg = data.get("message") or data.get("error") or str(data)
        assert expected_message in error_msg, \
            f"错误消息 '{error_msg}' 不包含期望内容 '{expected_message}'"
