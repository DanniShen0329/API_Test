# 接口自动化测试框架

基于 Python + pytest 的接口自动化测试框架，遵循统一的开发规范。

## 项目结构

```
.
├── tests/
│   ├── conftest.py              # 全局fixture配置
│   ├── config/                  # 环境配置目录
│   │   ├── __init__.py
│   │   ├── settings.py          # 基础配置类
│   │   ├── dev.py               # 开发环境配置
│   │   ├── test.py              # 测试环境配置
│   │   └── prod.py              # 生产环境配置
│   ├── data/                    # 测试数据目录
│   │   ├── __init__.py
│   │   └── price_group.json     # 价格组测试数据
│   ├── api/                     # API测试模块
│   │   ├── __init__.py
│   │   └── test_price_group_api.py
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       ├── http_client.py       # HTTP请求封装
│       └── assertions.py        # 断言工具
├── requirements.txt             # 依赖文件
├── pytest.ini                  # pytest配置
├── .env                        # 环境变量
└── README.md                   # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行冒烟测试
pytest -m smoke

# 运行集成测试
pytest -m integration

# 生成HTML报告
pytest --html=report.html --self-contained-html

# 并行执行
pytest -n auto

# 生成Allure报告
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## 配置说明

### 环境切换

通过 `TEST_ENV` 环境变量切换环境：

```bash
# 开发环境
set TEST_ENV=dev
pytest

# 测试环境
set TEST_ENV=test
pytest

# 生产环境（只读操作）
set TEST_ENV=prod
pytest
```

### 配置API认证

在 `.env` 文件中设置 `API_SID`：

```
API_SID=your-sid-here
```

## 代码规范

1. **测试函数命名**: 使用 `test_` 前缀 + 清晰描述
2. **Fixture管理**: 依赖项通过fixture注入
3. **数据驱动**: 使用 `@pytest.mark.parametrize`
4. **配置分离**: 禁止在测试文件中硬编码配置
5. **数据分离**: 测试数据放在 `data/` 目录

## 示例API测试

本框架包含价格组特价商品变更接口的测试示例：
- 有效的特价商品变更请求
- 批量变更测试
- 必填字段验证
- 数据格式验证
- 边界值测试
- 数据驱动测试
