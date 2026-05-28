from .models import Category
from .views import GetCart


def ShopNavigation(request):
    return {
        "NavigationCategories": Category.objects.all(),
        "CartCount": sum(GetCart(request).values()),
    }
