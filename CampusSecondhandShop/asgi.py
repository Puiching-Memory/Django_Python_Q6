"""ASGI config for CampusSecondhandShop."""
import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CampusSecondhandShop.settings")

application = get_asgi_application()
