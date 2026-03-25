"""测试数据加载器"""
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent


def load_json(filename: str) -> dict:
    """加载JSON测试数据文件"""
    filepath = DATA_DIR / filename
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


# 按模块组织数据
price_group_data = load_json("price_group.json")
