"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Add project root to Python path
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = get_asgi_application()
