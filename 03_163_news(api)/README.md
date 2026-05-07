# 网易新闻 API 接口分析系统

## 项目简介
本项目是一个模块化python爬虫，用于采集网易新闻首页动态记载新闻的标题信息，并持久化存储到MYSQL数据库中。项目通过api接口分析使用request库请求获取jsonp数据，工程化设计延用豆瓣项目，将配置管理，数据抓取，数据存储解耦为独立板块。

## 技术栈
- 语言:python 3
- 动态抓取:requests + api接口分析
- 解析库:正则表达式（剥离 JSONP 包裹） + json（解析 JSON 数据）
- 数据库:mysql+pymysql
- 反爬策略:User-Agent 伪装 + 随机时间间隔请求 +referer地址
  
## 项目结构
```
├── config.py #配置文件(数据库连接，请求头，爬取页数)
├── spider.py #数据请求与数据解析
├── storage.py #数据库初始化与数据存储模块
├── main.py #程序入口，调度抓取与存储流程
├── requirements.txt #项目依赖清单
└── README.md #项目文档说明
```

## 怎么开始

### 1.环境准备

```bash
# 克隆项目
git clone https://github.com/ty153/python_spider_lab

# 进入项目目录
cd python_spider_lab/03_163_news(api分析)

# 安装依赖
pip install -r requirements.txt

```

### 2.配置数据库
- 确保本地 MySQL 服务已启动,修改 config.py 中的数据库连接信息：
  
```python
CONFIG_MYSQL = {
    'host': 'localhost',
    'user': 'root',
    'password': '你的密码',
    'database': 'wangyi_news_api',      # 库名可自定义
    'charset': 'utf8mb4'
}
```
### 3.运行项目

```bash
python main.py
```

### 4.查看结果

```sql
USE wangyi_news_api;
SELECT * FROM new_titles LIMIT 10;
```

## 结果展示
| 运行过程                  | 数据库结果                 |
| ------------------------- | -------------------------- |
| ![运行](./images/run.png) | ![数据库](./images/db.png) |

## 数据字段说明
| 字段  | 说明     | 示例                                           |
| ----- | -------- | ---------------------------------------------- |
| title | 新闻标题 | 8岁女孩跟随邻居长江游泳溺亡 邻居曾抓住她又脱手 |


## 踩坑记录

1. JSONP 数据解析：接口返回的数据被 `data_callback(...)` 包裹，不能直接 `json.loads()`。通过 `re.search()` 正则提取括号内 JSON 字符串后，再用 `json.loads()` 解析成功。

2. 数据库存储类型和spider里返回的不同导致报错。通过统一数据类型为字典解决

3. main.py文件调用spider.py里的函数未传参导致错误。通过添加参数解决

4. 存储模块复用：从豆瓣项目复制 storage.py 时，发现只需修改 config.py 中的 TABLE_NAME 和 TABLE_COLUMNS 即可适配新项目，验证了通用模块设计的可行性。

## 核心设计

### 模块化架构
- config.py:统一管理配置，修改参数无需修改业务代码
- spider.py:专注于数据抓取与解析，返回标准化字典列表
- storage.py:自动及建立数据库，封装数据库操作
- main.py:调度各模块，包含异常处理与礼貌爬取延时

### 动态数据加载
- 通过 F12 Network 面板定位到新闻数据的 JSONP 接口
- 使用正则表达式去除接口返回的 callback 函数包裹，提取纯 JSON 字符串
- 通过 `json.loads()` 将 JSON 字符串解析为 Python 字典列表

### 通用储存模块(跨项目)
- storage.py 不包含任何业务字段，所有字段信息从 config.py 的 TABLE_COLUMNS 字典动态读取
- 建表 SQL 和插入 SQL 均自动生成，换项目只需修改 config.py，存储层代码零改动
- 通过 data.get(field, '') 安全取值，避免字段缺失导致程序崩溃

### 反爬策略
- refer的添加增添可信度
- User-Agent轮换,模仿多浏览器访问
- 随机访问间隔，模拟人类节奏

## 联系我
- 邮箱：3152057034@qq.com
- GitHub：https://github.com/ty153/python_spider_lab
- 博客：待更新