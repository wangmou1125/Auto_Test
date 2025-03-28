# 自动化测试框架

## 项目概述

这是一个基于Python的自动化测试框架，集成了API测试和UI测试功能，使用pytest作为测试执行引擎，allure作为测试报告生成工具。该框架采用了POM（Page Object Model）设计模式和数据驱动测试方法，旨在提供一个可扩展、易维护的测试解决方案。

## 项目结构

```
├── api_test/                # API测试相关代码
│   ├── api/                # API接口封装
│   │   ├── __init__.py
│   │   ├── base_api.py     # API基础类
│   │   └── login_api.py    # 登录API封装
│   └── data/               # API测试数据
│       └── login_api_data.yaml  # 登录API测试数据
├── common/                 # 公共模块
│   ├── config/             # 配置文件
│   │   ├── api_config.yaml # API测试配置
│   │   ├── logger.yaml     # 日志配置
│   │   └── ui_config.yaml  # UI测试配置
│   ├── model/              # 模型层
│   │   └── function.py     # 通用功能函数
│   └── utils/              # 工具类
│       ├── logger_util.py  # 日志工具
│       └── request_util.py # 请求工具
├── reports/                # 测试报告
│   ├── allure-report/      # Allure报告
│   ├── allure-results/     # Allure结果
│   ├── logs/               # 日志文件
│   └── screenshot/         # 截图文件
├── test/                   # 测试用例
│   ├── test_api/           # API测试用例
│   │   └── test_api_login.py  # 登录API测试
│   └── test_ui/            # UI测试用例
│       └── test_ui_login.py   # 登录UI测试
├── ui_test/                # UI测试相关代码
│   ├── data/               # UI测试数据
│   │   └── ui_login_data.csv  # 登录UI测试数据
│   └── page/               # 页面对象
│       ├── add_manage_page.py  # 管理页面
│       ├── base_page.py    # 基础页面类
│       └── login_page.py   # 登录页面
└── pytest.ini             # pytest配置文件
```

## 技术架构

### API测试架构

- **BaseApi类**：封装了基础的HTTP请求方法，处理请求和响应
- **业务API类**：继承BaseApi，封装具体业务接口的调用方法
- **测试数据**：使用YAML格式存储测试数据，实现数据驱动
- **测试用例**：使用pytest框架编写，通过参数化实现多场景测试

### UI测试架构

- **POM模式**：采用Page Object Model设计模式
  - **BasePage类**：封装基础页面操作方法
  - **业务页面类**：继承BasePage，封装具体页面元素和操作
- **测试数据**：使用CSV格式存储测试数据
- **测试用例**：使用pytest框架编写，通过fixture管理测试环境

### 公共模块

- **配置管理**：使用YAML格式管理配置信息
- **日志系统**：基于Python logging模块，支持控制台和文件输出
- **工具类**：封装通用功能，如数据读取、HTTP请求等

## 安装指南

### 环境要求

- Python 3.7+
- Chrome浏览器（UI测试）
- ChromeDriver（与Chrome版本匹配）

### 依赖安装

```bash
pip install -r requirements.txt  # 注意：项目中未包含此文件，需要自行创建
```

主要依赖包：
- pytest
- pytest-allure-adaptor
- selenium
- requests
- pyyaml

### ChromeDriver安装

1. 下载与Chrome浏览器版本匹配的ChromeDriver
2. 将ChromeDriver放入系统PATH路径或项目指定目录

## 使用指南

### 配置文件

在运行测试前，请先检查并修改配置文件：

- `common/config/api_config.yaml`：API测试配置，包含基础URL、超时时间等
- `common/config/ui_config.yaml`：UI测试配置，包含浏览器类型、URL等
- `common/config/logger.yaml`：日志配置

### 运行测试

#### 运行所有测试

```bash
pytest
```

#### 运行API测试

```bash
pytest test/test_api/
```

#### 运行UI测试

```bash
pytest test/test_ui/
```

#### 生成Allure报告

```bash
# 运行测试并生成结果
pytest --alluredir=reports/allure-results

# 生成HTML报告
allure generate reports/allure-results -o reports/allure-report --clean

# 查看报告
allure open reports/allure-report
```

### 添加新测试

#### 添加API测试

1. 在`api_test/api/`目录下创建新的API类
2. 在`api_test/data/`目录下添加测试数据
3. 在`test/test_api/`目录下创建测试用例文件

#### 添加UI测试

1. 在`ui_test/page/`目录下创建新的页面类
2. 在`ui_test/data/`目录下添加测试数据
3. 在`test/test_ui/`目录下创建测试用例文件

## 特性

- **数据驱动**：测试数据与测试逻辑分离，便于维护
- **POM模式**：UI测试采用Page Object Model，提高代码复用性
- **日志系统**：详细的日志记录，便于问题定位
- **截图功能**：UI测试失败自动截图
- **报告系统**：集成Allure报告，展示详细测试结果

## 注意事项

- 运行UI测试前确保Chrome浏览器和ChromeDriver已正确安装
- 确保测试环境网络可以访问被测系统
- 测试数据中的用户名密码需要与实际环境匹配