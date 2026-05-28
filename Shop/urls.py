from django.urls import path

from . import views


app_name = "Shop"

urlpatterns = [
    path("", views.ProductListView, name="ProductList"),
    path("assistant/", views.ShoppingAssistantView, name="ShoppingAssistant"),
    path("category/<slug:Slug>/", views.CategoryDetailView, name="CategoryDetail"),
    path("product/<int:ProductId>/", views.ProductDetailView, name="ProductDetail"),
    path("cart/", views.CartView, name="Cart"),
    path("cart/add/<int:ProductId>/", views.CartAddView, name="CartAdd"),
    path("cart/remove/<int:ProductId>/", views.CartRemoveView, name="CartRemove"),
    path("checkout/", views.CheckoutView, name="Checkout"),
    path("order/success/<int:OrderId>/", views.OrderSuccessView, name="OrderSuccess"),
]
