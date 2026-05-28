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

## 运行方式

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

打开浏览器访问：

```text
http://127.0.0.1:8000/
```

如果使用 `uv`，可执行：

```powershell
uv run --with django python manage.py migrate
uv run --with django python manage.py runserver
```

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
python manage.py createsuperuser
```
