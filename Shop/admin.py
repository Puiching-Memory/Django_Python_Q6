from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("Name", "Slug", "SortOrder")
    prepopulated_fields = {"Slug": ("Name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("Name", "Category", "Price", "Stock", "SellerName", "CreatedAt")
    list_filter = ("Category", "Condition")
    search_fields = ("Name", "SellerName", "Description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("ProductName", "UnitPrice", "Quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("OrderNumber", "ReceiverName", "Phone", "PaymentMethod", "TotalAmount", "CreatedAt")
    list_filter = ("PaymentMethod", "CreatedAt")
    search_fields = ("OrderNumber", "ReceiverName", "Phone")
    inlines = [OrderItemInline]
