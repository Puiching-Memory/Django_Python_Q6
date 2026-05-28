"""WSGI config for CampusSecondhandShop."""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CampusSecondhandShop.settings")

application = get_wsgi_application()
