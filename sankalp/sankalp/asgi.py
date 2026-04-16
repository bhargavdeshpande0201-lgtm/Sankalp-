"""
ASGI config for SANKALP project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sankalp.settings')

application = get_asgi_application()
