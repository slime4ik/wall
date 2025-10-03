from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Хранилища
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": "key",
            "secret_key": "key",
            "bucket_name": "name", 
            "endpoint_url": "url",
            "region_name": "ru-central1",
            "querystring_auth": True,
            "file_overwrite": False,
            "querystring_expire": 300,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = f"https://slime4ik-wallpaper-top.storage.yandexcloud.net/"

SECRET_KEY = 'django-insecure-MDWMIuhpjinp@@@!$#%&&%!@##!(*#!)(ke<@!'

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'silk',
    "corsheaders",
    'django_filters',
    # My apps
    'account',
    'image'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ROOT_URLCONF = 'supermaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / "templates/react",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [
    BASE_DIR / 'templates/react',
]

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

WSGI_APPLICATION = 'supermaster.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wallpaper',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 10*60
    }
}
# RATELIMIT_USE_CACHE = 'cache-for-ratelimiting'
# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 60*30
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'TaskManager API',
    'DESCRIPTION': 'Свагер для таск менеджера',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
