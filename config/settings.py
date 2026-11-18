import os

from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key

DEBUG = os.environ.get("ASSIGNMENT_DEBUG", "1") == "1"
SECRET_KEY = os.environ.get("ASSIGNMENT_SECRET_KEY")

if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Set ASSIGNMENT_SECRET_KEY when debug is disabled.")
    SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "estimator",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
STATIC_URL = "/static/"
