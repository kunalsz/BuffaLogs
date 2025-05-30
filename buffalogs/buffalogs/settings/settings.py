"""
Django settings for buffalogs project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

from .certego import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = CERTEGO_BUFFALOGS_SECRET_KEY
DEBUG = CERTEGO_DEBUG


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "impossible_travel",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "authentication",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "buffalogs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "buffalogs.wsgi.application"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"}, "reader_alert": {"format": "%(message)s"}},
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": os.path.join(CERTEGO_BUFFALOGS_LOG_PATH, "debug.log"),
            "encoding": "utf8",
            "maxBytes": 10485760,
            "backupCount": 4,
        },
    },
    "loggers": {
        "django": {"level": "DEBUG", "handlers": ["file_handler"], "propagate": True},
        "django.db.backends": {
            "handlers": ["null"],
            "propagate": False,
            "level": "DEBUG",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["file_handler"]},
    "urllib3.connectionpool": {
        "handlers": ["file_handler"],
        "level": "WARNING",
        "propagate": False,
    },
    "elasticsearch": {
        "handlers": ["file_handler"],
        "level": "WARNING",
        "propagate": False,
    },
    "pyquokka": {
        "handlers": ["file_handler"],
        "level": "WARNING",
        "propagate": False,
    },
    "routingfilter": {
        "handlers": ["file_handler"],
        "level": "WARNING",
        "propagate": False,
    },
}


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": CERTEGO_BUFFALOGS_POSTGRES_DB,
        "USER": CERTEGO_BUFFALOGS_POSTGRES_USER,
        "PASSWORD": CERTEGO_BUFFALOGS_POSTGRES_PASSWORD,
        "HOST": CERTEGO_BUFFALOGS_DB_HOSTNAME,
        "PORT": CERTEGO_BUFFALOGS_POSTGRES_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = CERTEGO_BUFFALOGS_STATIC_ROOT

SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=5),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # enables simple command line authentication
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 50,
}

AUTH_USER_MODEL = "authentication.User"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ["*"]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_NUMBER_FIELDS = None


# Celery config
CELERY_BROKER_URL = CERTEGO_BUFFALOGS_RABBITMQ_URI
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "celery.beat:PersistentScheduler"

CELERY_BEAT_SCHEDULE = {
    "process_logs": {
        "task": "BuffalogsProcessLogsTask",
        "schedule": crontab(minute=30),
    },
    "clean_models_periodically": {"task": "BuffalogsCleanModelsPeriodicallyTask", "schedule": crontab(hour=23, minute=59)},
    "notify_alerts": {"task": "NotifyAlertsTask", "schedule": crontab(minute=5)},
}
