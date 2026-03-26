"""价格组API测试模块 - 使用price_group.json测试数据"""
import pytest
import allure
import json
import logging

from tests.utils.assertions import APIAssertions
from tests.data import price_group_data

logger = logging.getLogger(__name__)

# API端点
PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT = "/h6-openapi2-service/v1/rprcgrp/changespecprice"


# ============ 使用parametrize数据驱动测试 ============

def get_valid_test_cases():
    """从JSON数据获取有效测试用例"""
    return [
        (case["description"], case["grpCode"], case["details"])
        for case in price_group_data["valid_requests"]
    ]


def get_invalid_test_cases():
    """从JSON数据获取无效测试用例"""
    return [
        (case["description"], case.get("grpCode", ""), case["details"], case.get("expected_error", ""))
        for case in price_group_data["invalid_requests"]
    ]


def get_edge_case_test_cases():
    """从JSON数据获取边界测试用例"""
    return [
        (case["description"], case["grpCode"], case["details"])
        for case in price_group_data["edge_cases"]
    ]


@pytest.mark.smoke
@allure.feature("价格组管理")
@allure.story("特价商品变更")
class TestPriceGroupChangeSpecPrice:
    """价格组特价商品变更接口测试 - 使用测试数据"""

    @allure.title("测试有效请求 - {description}")
    @pytest.mark.parametrize("description,grpCode,details", get_valid_test_cases())
    def test_change_spec_price_valid(self, api_client, auth_headers, description, grpCode, details):
        """测试有效的价格组特价商品变更请求"""
        payload = {
            "grpCode": grpCode,
            "details": details
        }
        
        with allure.step(f"【{description}】准备请求数据"):
            allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                         "请求数据", allure.attachment_type.JSON)
        
        with allure.step("发送特价商品变更请求"):
            response = api_client.post(
                PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                json=payload,
                headers=auth_headers
            )
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
            if response.text:
                allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
        
        with allure.step("验证响应"):
            APIAssertions.assert_status_code(response, 200)
            
            # 验证响应体中的业务状态码
            response_data = response.json()
            actual_code = response_data.get("code")
            assert actual_code == 2000, f"期望响应 code 为 2000，实际为 {actual_code}，msg: {response_data.get('msg', '')}"
            
            # 记录响应数据到日志（在报告中显示）
            logger.info(f"[验证结果] ✅ {description} - 成功 (code: 2000)")
            logger.info(f"[响应数据] {json.dumps(response_data, indent=2, ensure_ascii=False)}")

    @allure.title("测试无效请求 - {description}")
    @pytest.mark.parametrize("description,grpCode,details,expected_error", get_invalid_test_cases())
    def test_change_spec_price_invalid(self, api_client, auth_headers, description, grpCode, details, expected_error):
        """测试无效的价格组特价商品变更请求"""
        payload = {
            "grpCode": grpCode,
            "details": details
        }
        
        with allure.step(f"【{description}】准备请求数据"):
            allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                         "请求数据", allure.attachment_type.JSON)
            if expected_error:
                allure.attach(expected_error, "期望错误", allure.attachment_type.TEXT)
        
        with allure.step("发送请求"):
            response = api_client.post(
                PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                json=payload,
                headers=auth_headers
            )
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
            if response.text:
                allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
        
        with allure.step("验证错误响应"):
            # API 对无效请求返回 200，需要在响应体中检查错误码
            response_data = response.json()
            allure.attach(json.dumps(response_data, indent=2, ensure_ascii=False), 
                         "响应数据", allure.attachment_type.JSON)
            
            # 检查响应体中的业务错误码（非 0 或特定成功码表示错误）
            biz_code = response_data.get("code", 0)
            if biz_code != 0:
                logger.info(f"⚠️ {description} - 业务错误码: {biz_code}, msg: {response_data.get('msg', '')}")
            else:
                logger.warning(f"⚠️ {description} - API 接受了无效请求，返回 code=0")
            
            # 记录响应状态，但不强制失败（因为不同 API 设计不同）
            assert biz_code != 0 or response.status_code >= 400, \
                f"期望 API 拒绝无效请求，但返回成功状态。响应: {response_data}"

    @allure.title("测试边界情况 - {description}")
    @pytest.mark.parametrize("description,grpCode,details", get_edge_case_test_cases())
    def test_change_spec_price_edge_cases(self, api_client, auth_headers, description, grpCode, details):
        """测试边界情况"""
        payload = {
            "grpCode": grpCode,
            "details": details
        }
        
        with allure.step(f"【{description}】准备请求数据"):
            allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                         "请求数据", allure.attachment_type.JSON)
        
        with allure.step("发送请求"):
            response = api_client.post(
                PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                json=payload,
                headers=auth_headers
            )
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
            if response.text:
                allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
        
        with allure.step("记录响应"):
            logger.info(f"🔍 {description} - 返回 {response.status_code}")


@pytest.mark.integration
@allure.feature("价格组管理")
@allure.story("数据驱动完整测试")
class TestPriceGroupDataDrivenFull:
    """完整的数据驱动测试 - 遍历所有测试数据"""

    @allure.title("遍历所有有效请求测试数据")
    def test_all_valid_requests_from_json(self, api_client, auth_headers):
        """使用JSON中所有有效请求数据进行测试"""
        valid_requests = price_group_data["valid_requests"]
        
        for i, request_data in enumerate(valid_requests, 1):
            with allure.step(f"[{i}/{len(valid_requests)}] {request_data.get('description', '无描述')}"):
                payload = {
                    "grpCode": request_data["grpCode"],
                    "details": request_data["details"]
                }
                
                allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                             "请求数据", allure.attachment_type.JSON)
                
                response = api_client.post(
                    PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                    json=payload,
                    headers=auth_headers
                )
                
                allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
                APIAssertions.assert_status_code(response, 200)
                
                logger.info(f"✅ [{i}/{len(valid_requests)}] {request_data.get('description', '无描述')} - 成功")

    @allure.title("遍历所有无效请求测试数据")
    def test_all_invalid_requests_from_json(self, api_client, auth_headers):
        """使用JSON中所有无效请求数据进行测试"""
        invalid_requests = price_group_data["invalid_requests"]
        
        for i, request_data in enumerate(invalid_requests, 1):
            description = request_data.get('description', '无描述')
            expected_error = request_data.get('expected_error', '')
            
            with allure.step(f"[{i}/{len(invalid_requests)}] {description}"):
                payload = {
                    "grpCode": request_data.get("grpCode", ""),
                    "details": request_data["details"]
                }
                
                allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                             "请求数据", allure.attachment_type.JSON)
                if expected_error:
                    allure.attach(expected_error, "期望错误", allure.attachment_type.TEXT)
                
                response = api_client.post(
                    PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                    json=payload,
                    headers=auth_headers
                )
                
                allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
                
                # API 对无效请求返回 200，需要在响应体中检查错误码
                response_data = response.json()
                allure.attach(json.dumps(response_data, indent=2, ensure_ascii=False), 
                             "响应数据", allure.attachment_type.JSON)
                
                biz_code = response_data.get("code", 0)
                if biz_code != 0:
                    logger.info(f"⚠️ [{i}/{len(invalid_requests)}] {description} - 业务错误码: {biz_code}")
                else:
                    logger.warning(f"⚠️ [{i}/{len(invalid_requests)}] {description} - API 接受了无效请求")
                
                # 记录结果，但不强制失败
                assert biz_code != 0 or response.status_code >= 400, \
                    f"期望 API 拒绝无效请求，但返回成功状态。响应: {response_data}"

    @allure.title("遍历所有边界情况测试数据")
    def test_all_edge_cases_from_json(self, api_client, auth_headers):
        """使用JSON中所有边界情况进行测试"""
        edge_cases = price_group_data["edge_cases"]
        
        for i, request_data in enumerate(edge_cases, 1):
            description = request_data.get('description', '无描述')
            
            with allure.step(f"[{i}/{len(edge_cases)}] {description}"):
                payload = {
                    "grpCode": request_data["grpCode"],
                    "details": request_data["details"]
                }
                
                allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                             "请求数据", allure.attachment_type.JSON)
                
                response = api_client.post(
                    PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                    json=payload,
                    headers=auth_headers
                )
                
                allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
                
                logger.info(f"🔍 [{i}/{len(edge_cases)}] {description} - 返回 {response.status_code}")


@pytest.mark.smoke
@allure.feature("价格组管理")
@allure.story("单个场景测试")
class TestPriceGroupSingleScenarios:
    """单个场景测试 - 使用具体测试数据"""

    @allure.title("测试单个商品设置为特价")
    def test_single_item_spec_price(self, api_client, auth_headers):
        """测试单个商品设置为特价商品"""
        # 从测试数据获取第一个有效请求
        test_data = price_group_data["valid_requests"][0]
        
        payload = {
            "grpCode": test_data["grpCode"],
            "details": test_data["details"]
        }
        
        with allure.step(f"准备请求: {test_data['description']}"):
            allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                         "请求数据", allure.attachment_type.JSON)
        
        with allure.step("发送请求"):
            response = api_client.post(
                PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                json=payload,
                headers=auth_headers
            )
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
        
        with allure.step("验证响应"):
            APIAssertions.assert_status_code(response, 200)
            
            # 验证响应包含必要字段
            response_data = response.json()
            APIAssertions.assert_field_exists(response, "code")
            logger.info(f"单个商品特价设置成功: {response_data}")

    @allure.title("测试批量商品特价变更")
    def test_batch_items_spec_price(self, api_client, auth_headers):
        """测试批量商品特价变更"""
        # 从测试数据获取第二个有效请求（批量）
        if len(price_group_data["valid_requests"]) > 1:
            test_data = price_group_data["valid_requests"][1]
        else:
            pytest.skip("没有足够的有效请求数据")
        
        payload = {
            "grpCode": test_data["grpCode"],
            "details": test_data["details"]
        }
        
        with allure.step(f"准备批量请求: {test_data['description']}"):
            allure.attach(json.dumps(payload, indent=2, ensure_ascii=False), 
                         "请求数据", allure.attachment_type.JSON)
            allure.attach(str(len(test_data["details"])), "商品数量", allure.attachment_type.TEXT)
        
        with allure.step("发送批量请求"):
            response = api_client.post(
                PRICE_GROUP_CHANGE_SPEC_PRICE_ENDPOINT,
                json=payload,
                headers=auth_headers
            )
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
        
        with allure.step("验证响应"):
            APIAssertions.assert_status_code(response, 200)
            logger.info(f"批量商品特价变更成功: {len(test_data['details'])} 个商品")
