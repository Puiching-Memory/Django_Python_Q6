#!/usr/bin/env python
"""Django command-line utility for CampusSecondhandShop."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CampusSecondhandShop.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Could not import Django. Install dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
