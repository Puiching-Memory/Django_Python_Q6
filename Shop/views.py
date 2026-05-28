from decimal import Decimal
from uuid import uuid4

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CheckoutForm
from .models import Category, Order, OrderItem, Product
from .shopping_agent import RunShoppingAssistantAgent


CartSessionKey = "CampusSecondhandCart"
AssistantSessionKey = "CampusSecondhandAssistant"


def GetCart(request):
    return request.session.get(CartSessionKey, {})


def SaveCart(request, cart):
    request.session[CartSessionKey] = cart
    request.session.modified = True


def BuildCartItems(cart):
    product_ids = [int(ProductId) for ProductId in cart.keys()]
    products = Product.objects.filter(pk__in=product_ids).select_related("Category")
    items = []
    total = Decimal("0.00")

    for product in products:
        quantity = int(cart.get(str(product.pk), 0))
        if quantity <= 0:
            continue
        subtotal = product.Price * quantity
        total += subtotal
        items.append(
            {
                "Product": product,
                "Quantity": quantity,
                "Subtotal": subtotal,
            }
        )
    return items, total


def GetAssistantHistory(request):
    return request.session.get(AssistantSessionKey, [])


def SaveAssistantHistory(request, history):
    request.session[AssistantSessionKey] = history[-8:]
    request.session.modified = True


def ProductListView(request):
    categories = Category.objects.prefetch_related("Products")
    newest_products = Product.objects.select_related("Category")[:8]
    return render(
        request,
        "Shop/ProductList.html",
        {
            "Categories": categories,
            "NewestProducts": newest_products,
        },
    )


def ShoppingAssistantView(request):
    question = ""
    if request.method == "POST" and request.POST.get("Action") == "Clear":
        SaveAssistantHistory(request, [])
        return redirect("Shop:ShoppingAssistant")

    if request.method == "POST":
        question = request.POST.get("Question", "").strip()[:160]
        if not question:
            messages.warning(request, "请输入预算、用途或想购买的商品。")

    plan = RunShoppingAssistantAgent(question, GetCart(request))
    history = GetAssistantHistory(request)
    if request.method == "POST" and question:
        history = history + [
            {"Role": "user", "Text": question},
            {"Role": "assistant", "Text": plan["Reply"]},
        ]
        SaveAssistantHistory(request, history)
        history = GetAssistantHistory(request)

    return render(
        request,
        "Shop/ShoppingAssistant.html",
        {
            "Question": question,
            "AssistantReply": plan["Reply"],
            "AssistantTags": plan["Tags"],
            "Recommendations": plan["Recommendations"],
            "AssistantHistory": history,
            "AgentTrace": plan["Trace"],
            "AgentTools": plan["Tools"],
            "AgentFramework": plan["Framework"],
        },
    )


def CategoryDetailView(request, Slug):
    category = get_object_or_404(Category, Slug=Slug)
    products = category.Products.select_related("Category").all()
    return render(
        request,
        "Shop/CategoryDetail.html",
        {
            "Category": category,
            "Products": products,
        },
    )


def ProductDetailView(request, ProductId):
    product = get_object_or_404(Product.objects.select_related("Category"), pk=ProductId)
    related_products = (
        Product.objects.filter(Category=product.Category)
        .exclude(pk=product.pk)
        .select_related("Category")[:4]
    )
    return render(
        request,
        "Shop/ProductDetail.html",
        {
            "Product": product,
            "RelatedProducts": related_products,
        },
    )


@require_POST
def CartAddView(request, ProductId):
    product = get_object_or_404(Product, pk=ProductId)
    try:
        quantity = int(request.POST.get("Quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    quantity = max(1, min(quantity, product.Stock))
    cart = GetCart(request)
    current_quantity = int(cart.get(str(product.pk), 0))
    cart[str(product.pk)] = min(product.Stock, current_quantity + quantity)
    SaveCart(request, cart)
    messages.success(request, f"已将 {product.Name} 加入购物车。")
    return redirect(request.POST.get("Next") or reverse("Shop:Cart"))


def CartView(request):
    cart = GetCart(request)
    items, total = BuildCartItems(cart)
    return render(
        request,
        "Shop/Cart.html",
        {
            "CartItems": items,
            "TotalAmount": total,
        },
    )


@require_POST
def CartRemoveView(request, ProductId):
    cart = GetCart(request)
    product_name = ""
    try:
        product = Product.objects.get(pk=ProductId)
        product_name = product.Name
    except Product.DoesNotExist:
        pass
    cart.pop(str(ProductId), None)
    SaveCart(request, cart)
    if product_name:
        messages.info(request, f"已删除购物车中的 {product_name}。")
    return redirect("Shop:Cart")


def CheckoutView(request):
    cart = GetCart(request)
    items, total = BuildCartItems(cart)
    if not items:
        messages.warning(request, "购物车为空，请先选择商品。")
        return redirect("Shop:ProductList")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.OrderNumber = f"CS{uuid4().hex[:12].upper()}"
            order.TotalAmount = total
            order.save()

            for item in items:
                product = item["Product"]
                OrderItem.objects.create(
                    Order=order,
                    Product=product,
                    ProductName=product.Name,
                    UnitPrice=product.Price,
                    Quantity=item["Quantity"],
                )

            SaveCart(request, {})
            return redirect("Shop:OrderSuccess", OrderId=order.pk)
    else:
        form = CheckoutForm()

    return render(
        request,
        "Shop/Checkout.html",
        {
            "Form": form,
            "CartItems": items,
            "TotalAmount": total,
        },
    )


def OrderSuccessView(request, OrderId):
    order = get_object_or_404(Order.objects.prefetch_related("Items"), pk=OrderId)
    return render(
        request,
        "Shop/OrderSuccess.html",
        {
            "Order": order,
            "OrderItems": order.Items.all(),
        },
    )
