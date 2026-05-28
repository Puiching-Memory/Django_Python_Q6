from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("Name", models.CharField(max_length=40, unique=True, verbose_name="分类名称")),
                ("Slug", models.SlugField(max_length=50, unique=True, verbose_name="访问标识")),
                ("Description", models.CharField(blank=True, max_length=160, verbose_name="分类说明")),
                ("SortOrder", models.PositiveIntegerField(default=0, verbose_name="排序")),
            ],
            options={
                "verbose_name": "商品分类",
                "verbose_name_plural": "商品分类",
                "ordering": ["SortOrder", "Name"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("OrderNumber", models.CharField(max_length=32, unique=True, verbose_name="订单编号")),
                ("ReceiverName", models.CharField(max_length=40, verbose_name="收货人")),
                ("Phone", models.CharField(max_length=20, verbose_name="联系电话")),
                ("Address", models.CharField(max_length=160, verbose_name="收货地址")),
                (
                    "PaymentMethod",
                    models.CharField(
                        choices=[("Wechat", "微信支付"), ("Alipay", "支付宝"), ("Cash", "线下当面支付")],
                        max_length=20,
                        verbose_name="支付方式",
                    ),
                ),
                ("Remark", models.CharField(blank=True, max_length=200, verbose_name="订单备注")),
                ("TotalAmount", models.DecimalField(decimal_places=2, default="0.00", max_digits=10, verbose_name="订单金额")),
                ("CreatedAt", models.DateTimeField(auto_now_add=True, verbose_name="提交时间")),
            ],
            options={
                "verbose_name": "订单",
                "verbose_name_plural": "订单",
                "ordering": ["-CreatedAt"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("Name", models.CharField(max_length=80, verbose_name="商品名称")),
                ("SellerName", models.CharField(max_length=40, verbose_name="卖家")),
                ("Condition", models.CharField(max_length=40, verbose_name="成色")),
                ("Price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="价格")),
                ("Stock", models.PositiveIntegerField(default=1, verbose_name="库存")),
                ("ImageName", models.CharField(max_length=80, verbose_name="图片文件")),
                ("Description", models.TextField(verbose_name="商品详情")),
                ("CreatedAt", models.DateTimeField(auto_now_add=True, verbose_name="发布时间")),
                (
                    "Category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Products",
                        to="Shop.category",
                        verbose_name="所属分类",
                    ),
                ),
            ],
            options={
                "verbose_name": "商品",
                "verbose_name_plural": "商品",
                "ordering": ["-CreatedAt", "Name"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ProductName", models.CharField(max_length=80, verbose_name="商品名称")),
                ("UnitPrice", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="单价")),
                ("Quantity", models.PositiveIntegerField(verbose_name="数量")),
                (
                    "Order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Items",
                        to="Shop.order",
                        verbose_name="订单",
                    ),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="OrderItems",
                        to="Shop.product",
                        verbose_name="商品",
                    ),
                ),
            ],
            options={
                "verbose_name": "订单明细",
                "verbose_name_plural": "订单明细",
            },
        ),
    ]
