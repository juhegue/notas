"""
WSGI config for notas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append("/var/www/notas/")
sys.path.append("/home/juan/.virtualenvs/notas/lib/python3.8/site-packages/")

os.environ.setdefault("LANG", "en_US.UTF-8")
os.environ.setdefault("LC_ALL", "en_US.UTF-8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notas.settings_pro")

application = get_wsgi_application()
