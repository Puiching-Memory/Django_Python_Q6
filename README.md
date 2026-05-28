# Django_Python_Q6

基于 Django 的校园二手交易购物平台设计与实现。

## 项目功能

本项目围绕课程期末大作业要求实现 6 个页面：

1. 商品展示页面：展示商品分类和最新商品。
2. 商品分类展示页面：展示某一分类下的全部商品。
3. 商品详情页面：展示商品价格、成色、库存、卖家和详情信息。
4. 购物车页面：展示购物车商品，统计金额，并支持删除购物车物品。
5. 订单提交页面：展示已选商品列表、订单信息和支付方式。
6. 订单提交成功页面：展示订单商品、订单信息和商品金额统计。

自定义功能：后台管理、示例商品数据、订单编号生成、同类商品推荐、消息提示。

## DeepSeek Agent 配置

购物助手通过 LangGraph 编排工具节点，并可读取 `.env` 调用 DeepSeek API 生成回复。首次运行前复制示例配置：

```powershell
copy .env.example .env
```

然后在 `.env` 中填写：

```env
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_API_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_THINKING_TYPE=disabled
DEEPSEEK_REASONING_EFFORT=high
DEEPSEEK_TIMEOUT_SECONDS=15
```

DeepSeek V4 当前推荐模型为 `deepseek-v4-flash` 或 `deepseek-v4-pro`，旧的 `deepseek-chat` / `deepseek-reasoner` 将于 2026-07-24 停用。购物助手默认使用 `deepseek-v4-flash` 的 non-thinking 模式；如需推理模式，可将 `DEEPSEEK_THINKING_TYPE` 改为 `enabled`。

未配置 `DEEPSEEK_API_KEY` 时，购物助手会自动使用本地规则推荐兜底。

## 运行方式

### 方式一：本地运行与测试（uv）

```powershell
uv sync
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py runserver
```

打开浏览器访问：

```text
http://127.0.0.1:8000/
```

常用管理命令也通过 `uv run` 执行：

```powershell
uv run python manage.py createsuperuser
```

### 方式二：线上/容器测试（Docker）

项目已内置 Dockerfile 和 docker-compose.yml，可通过 Docker 一键启动：

```powershell
# 构建镜像
docker compose build

# 容器环境检查
docker compose run --rm web python manage.py check

# 启动容器
docker compose up --build

# 后台运行
docker compose up --build -d

# 停止容器
docker compose down
```

启动后访问：

```text
http://localhost:8000/
```

> 说明：容器启动时会自动执行 `migrate`，数据文件 `db.sqlite3` 通过挂载卷持久化到宿主机。

## 项目结构

```text
CampusSecondhandShop/   Django 项目配置
Shop/                   购物平台应用、模型、视图、表单、路由
templates/Shop/         页面模板
static/css/             样式文件
static/images/          本地商品示意图
docs/                   课程任务文档和考核报告
```

## 管理后台

项目已注册分类、商品、订单和订单明细模型。可创建管理员账号后登录后台维护数据：

```powershell
uv run python manage.py createsuperuser
```
