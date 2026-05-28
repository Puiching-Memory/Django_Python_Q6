from decimal import Decimal

from django.db import models
from django.urls import reverse


class Category(models.Model):
    Name = models.CharField("分类名称", max_length=40, unique=True)
    Slug = models.SlugField("访问标识", max_length=50, unique=True)
    Description = models.CharField("分类说明", max_length=160, blank=True)
    SortOrder = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ["SortOrder", "Name"]
        verbose_name = "商品分类"
        verbose_name_plural = "商品分类"

    def __str__(self):
        return self.Name

    def GetAbsoluteUrl(self):
        return reverse("Shop:CategoryDetail", kwargs={"Slug": self.Slug})


class Product(models.Model):
    Category = models.ForeignKey(
        Category,
        verbose_name="所属分类",
        related_name="Products",
        on_delete=models.CASCADE,
    )
    Name = models.CharField("商品名称", max_length=80)
    SellerName = models.CharField("卖家", max_length=40)
    Condition = models.CharField("成色", max_length=40)
    Price = models.DecimalField("价格", max_digits=8, decimal_places=2)
    Stock = models.PositiveIntegerField("库存", default=1)
    ImageName = models.CharField("图片文件", max_length=80)
    Description = models.TextField("商品详情")
    CreatedAt = models.DateTimeField("发布时间", auto_now_add=True)

    class Meta:
        ordering = ["-CreatedAt", "Name"]
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.Name

    def GetAbsoluteUrl(self):
        return reverse("Shop:ProductDetail", kwargs={"ProductId": self.pk})


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("Wechat", "微信支付"),
        ("Alipay", "支付宝"),
        ("Cash", "线下当面支付"),
    ]

    OrderNumber = models.CharField("订单编号", max_length=32, unique=True)
    ReceiverName = models.CharField("收货人", max_length=40)
    Phone = models.CharField("联系电话", max_length=20)
    Address = models.CharField("收货地址", max_length=160)
    PaymentMethod = models.CharField("支付方式", max_length=20, choices=PAYMENT_CHOICES)
    Remark = models.CharField("订单备注", max_length=200, blank=True)
    TotalAmount = models.DecimalField("订单金额", max_digits=10, decimal_places=2, default=Decimal("0.00"))
    CreatedAt = models.DateTimeField("提交时间", auto_now_add=True)

    class Meta:
        ordering = ["-CreatedAt"]
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def __str__(self):
        return self.OrderNumber

    def PaymentMethodText(self):
        return dict(self.PAYMENT_CHOICES).get(self.PaymentMethod, self.PaymentMethod)


class OrderItem(models.Model):
    Order = models.ForeignKey(
        Order,
        verbose_name="订单",
        related_name="Items",
        on_delete=models.CASCADE,
    )
    Product = models.ForeignKey(
        Product,
        verbose_name="商品",
        related_name="OrderItems",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    ProductName = models.CharField("商品名称", max_length=80)
    UnitPrice = models.DecimalField("单价", max_digits=8, decimal_places=2)
    Quantity = models.PositiveIntegerField("数量")

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = "订单明细"

    def __str__(self):
        return f"{self.ProductName} x {self.Quantity}"

    @property
    def Subtotal(self):
        return self.UnitPrice * self.Quantity
