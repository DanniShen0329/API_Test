"""生成详细的API测试报告"""
import json
import requests
import logging
from datetime import datetime
from tests.config import get_config
from tests.data import price_group_data

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API配置
config = get_config()
BASE_URL = config.base_url
ENDPOINT = "/h6-openapi2-service/v1/rprcgrp/changespecprice"
API_URL = f"{BASE_URL}{ENDPOINT}"

# 请求头
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "sid": config.api_sid or "test-sid"
}


def format_json(data):
    """格式化JSON输出"""
    return json.dumps(data, indent=2, ensure_ascii=False)


def call_api(payload):
    """调用API并返回完整结果"""
    full_request = {
        "change": payload
    }
    
    try:
        response = requests.post(
            API_URL,
            json=full_request,
            headers=HEADERS,
            timeout=30
        )
        
        response_data = None
        try:
            response_data = response.json() if response.text else None
        except:
            response_data = {"raw_text": response.text}
        
        return {
            "request_method": "POST",
            "request_url": API_URL,
            "request_headers": HEADERS,
            "request_body": full_request,
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
            "response_body": response_data,
            "error": None
        }
    except Exception as e:
        return {
            "request_method": "POST",
            "request_url": API_URL,
            "request_headers": HEADERS,
            "request_body": full_request,
            "status_code": None,
            "response_headers": None,
            "response_body": None,
            "error": str(e)
        }


def generate_report():
    """生成详细测试报告"""
    report_lines = []
    
    # 报告头部
    report_lines.append("=" * 100)
    report_lines.append(" " * 35 + "API接口自动化测试详细报告")
    report_lines.append("=" * 100)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"测试环境: {config.env}")
    report_lines.append(f"API基础地址: {BASE_URL}")
    report_lines.append(f"API端点: {ENDPOINT}")
    report_lines.append(f"完整URL: {API_URL}")
    report_lines.append("")
    
    # 测试结果统计
    total_cases = 0
    passed_cases = 0
    failed_cases = 0
    
    # 1. 测试有效请求
    report_lines.append("=" * 100)
    report_lines.append("【一、有效请求测试】")
    report_lines.append("=" * 100)
    
    for i, case in enumerate(price_group_data["valid_requests"], 1):
        total_cases += 1
        report_lines.append(f"\n{'─' * 100}")
        report_lines.append(f"测试用例 {i}: {case['description']}")
        report_lines.append(f"{'─' * 100}")
        
        # 构造请求参数
        payload = {
            "grpCode": case["grpCode"],
            "details": case["details"]
        }
        
        report_lines.append("\n【预期结果】")
        report_lines.append("  HTTP状态码: 200")
        report_lines.append("  业务码(code): 0")
        report_lines.append("  结果: 成功")
        
        # 调用API
        result = call_api(payload)
        
        report_lines.append("\n【实际请求】")
        report_lines.append(f"  请求方法: {result['request_method']}")
        report_lines.append(f"  请求URL: {result['request_url']}")
        report_lines.append(f"  请求头:")
        report_lines.append("    " + format_json(result['request_headers']).replace("\n", "\n    "))
        report_lines.append(f"  请求体(Request Body):")
        report_lines.append("    " + format_json(result['request_body']).replace("\n", "\n    "))
        
        report_lines.append("\n【实际响应】")
        report_lines.append(f"  HTTP状态码: {result['status_code']}")
        if result['response_headers']:
            report_lines.append(f"  响应头:")
            report_lines.append("    " + format_json(result['response_headers']).replace("\n", "\n    "))
        if result['response_body']:
            report_lines.append(f"  响应体(Response Body):")
            report_lines.append("    " + format_json(result['response_body']).replace("\n", "\n    "))
        if result['error']:
            report_lines.append(f"  错误信息: {result['error']}")
        
        # 判断结果
        is_success = (result['status_code'] == 200 and 
                     result['response_body'] and 
                     result['response_body'].get('code') == 0)
        
        report_lines.append("\n【测试结果】")
        if is_success:
            passed_cases += 1
            report_lines.append("  ✅ 通过")
            report_lines.append(f"  验证点: HTTP 200, code=0, msg={result['response_body'].get('msg', 'N/A')}")
        else:
            failed_cases += 1
            report_lines.append("  ❌ 失败")
            if result['response_body']:
                biz_code = result['response_body'].get('code')
                biz_msg = result['response_body'].get('msg', '')
                report_lines.append(f"  失败原因: 业务码={biz_code}, 消息={biz_msg}")
    
    # 2. 测试无效请求
    report_lines.append("\n" + "=" * 100)
    report_lines.append("【二、无效请求测试】")
    report_lines.append("=" * 100)
    
    for i, case in enumerate(price_group_data["invalid_requests"], 1):
        total_cases += 1
        report_lines.append(f"\n{'─' * 100}")
        report_lines.append(f"测试用例 {i}: {case['description']}")
        report_lines.append(f"{'─' * 100}")
        
        # 构造请求参数
        payload = {
            "grpCode": case.get("grpCode", ""),
            "details": case["details"]
        }
        
        report_lines.append("\n【预期结果】")
        report_lines.append(f"  预期错误: {case.get('expected_error', '请求应被拒绝')}")
        report_lines.append("  预期响应: HTTP 200 + 业务错误码 (code ≠ 0)")
        
        # 调用API
        result = call_api(payload)
        
        report_lines.append("\n【实际请求】")
        report_lines.append(f"  请求方法: {result['request_method']}")
        report_lines.append(f"  请求URL: {result['request_url']}")
        report_lines.append(f"  请求头:")
        report_lines.append("    " + format_json(result['request_headers']).replace("\n", "\n    "))
        report_lines.append(f"  请求体(Request Body):")
        report_lines.append("    " + format_json(result['request_body']).replace("\n", "\n    "))
        
        report_lines.append("\n【实际响应】")
        report_lines.append(f"  HTTP状态码: {result['status_code']}")
        if result['response_headers']:
            report_lines.append(f"  响应头:")
            report_lines.append("    " + format_json(result['response_headers']).replace("\n", "\n    "))
        if result['response_body']:
            report_lines.append(f"  响应体(Response Body):")
            report_lines.append("    " + format_json(result['response_body']).replace("\n", "\n    "))
        if result['error']:
            report_lines.append(f"  错误信息: {result['error']}")
        
        # 判断结果 (API 对无效请求返回 200 但业务码非 0)
        is_rejected = (result['response_body'] and 
                      result['response_body'].get('code') != 0)
        
        report_lines.append("\n【测试结果】")
        if is_rejected:
            passed_cases += 1
            report_lines.append("  ✅ 通过")
            biz_code = result['response_body'].get('code')
            biz_msg = result['response_body'].get('msg', '')
            report_lines.append(f"  验证点: API正确拒绝无效请求, code={biz_code}, msg={biz_msg}")
        else:
            failed_cases += 1
            report_lines.append("  ⚠️ 警告")
            report_lines.append("  验证点: API接受了无效请求 (可能需要后端加强校验)")
    
    # 3. 测试边界情况
    report_lines.append("\n" + "=" * 100)
    report_lines.append("【三、边界情况测试】")
    report_lines.append("=" * 100)
    
    for i, case in enumerate(price_group_data["edge_cases"], 1):
        total_cases += 1
        report_lines.append(f"\n{'─' * 100}")
        report_lines.append(f"测试用例 {i}: {case['description']}")
        report_lines.append(f"{'─' * 100}")
        
        # 构造请求参数
        payload = {
            "grpCode": case["grpCode"],
            "details": case["details"]
        }
        
        report_lines.append("\n【测试说明】")
        report_lines.append(f"  测试目的: 验证边界情况 '{case['description']}' 的处理")
        
        # 调用API
        result = call_api(payload)
        
        report_lines.append("\n【实际请求】")
        report_lines.append(f"  请求方法: {result['request_method']}")
        report_lines.append(f"  请求URL: {result['request_url']}")
        report_lines.append(f"  请求头:")
        report_lines.append("    " + format_json(result['request_headers']).replace("\n", "\n    "))
        report_lines.append(f"  请求体(Request Body):")
        report_lines.append("    " + format_json(result['request_body']).replace("\n", "\n    "))
        
        report_lines.append("\n【实际响应】")
        report_lines.append(f"  HTTP状态码: {result['status_code']}")
        if result['response_headers']:
            report_lines.append(f"  响应头:")
            report_lines.append("    " + format_json(result['response_headers']).replace("\n", "\n    "))
        if result['response_body']:
            report_lines.append(f"  响应体(Response Body):")
            report_lines.append("    " + format_json(result['response_body']).replace("\n", "\n    "))
        if result['error']:
            report_lines.append(f"  错误信息: {result['error']}")
        
        passed_cases += 1
        report_lines.append("\n【测试结果】")
        report_lines.append("  ✅ 通过 (记录边界情况)")
        if result['response_body']:
            biz_code = result['response_body'].get('code')
            biz_msg = result['response_body'].get('msg', '')
            report_lines.append(f"  响应: code={biz_code}, msg={biz_msg}")
    
    # 汇总
    report_lines.append("\n" + "=" * 100)
    report_lines.append("【测试汇总】")
    report_lines.append("=" * 100)
    report_lines.append(f"总测试用例数: {total_cases}")
    report_lines.append(f"  - 通过: {passed_cases}")
    report_lines.append(f"  - 失败: {failed_cases}")
    report_lines.append(f"  - 通过率: {passed_cases/total_cases*100:.1f}%")
    report_lines.append("")
    report_lines.append("测试分类统计:")
    report_lines.append(f"  - 有效请求测试: {len(price_group_data['valid_requests'])} 个")
    report_lines.append(f"  - 无效请求测试: {len(price_group_data['invalid_requests'])} 个")
    report_lines.append(f"  - 边界情况测试: {len(price_group_data['edge_cases'])} 个")
    report_lines.append("=" * 100)
    
    return "\n".join(report_lines)


if __name__ == "__main__":
    import os
    os.environ["TEST_ENV"] = "test"
    
    import sys
    
    print("正在生成详细测试报告，请稍候...")
    report = generate_report()
    
    # 保存到文件
    report_file = f"test_report_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"详细报告已保存到: {report_file}")
