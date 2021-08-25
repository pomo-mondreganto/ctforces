import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get('DJANGO_DEBUG') == '1'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'testing')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'django_redis',
    'stdimage',
    'guardian',
    'corsheaders',
    'rest_framework_tricks',
    'rest_framework_nested',
    'django_filters',
    'silk',

    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'silk.middleware.SilkyMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ctforces.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ctforces.wsgi.application'

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

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'api.User'
APPEND_SLASH = False

AUTHENTICATION_BACKENDS = [
    'api.backends.CustomAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}

AMQP_USER = os.environ['RABBITMQ_DEFAULT_USER']
AMQP_PASS = os.environ['RABBITMQ_DEFAULT_PASS']
AMQP_VHOST = os.environ['RABBITMQ_DEFAULT_VHOST']
AMQP_HOST = os.environ['RABBITMQ_HOST']
AMQP_PORT = os.environ['RABBITMQ_PORT']

REDIS_HOST = 'redis'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s [%(asctime)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "ctforces-cache"
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSIONS_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://127.0.0.1:\d+$",
]

EMAIL_MODE = os.environ.get('DJANGO_EMAIL_MODE')
EMAIL_ENABLED = EMAIL_MODE in ['smtp', 'sendgrid']
EMAIL_URL = os.environ['DJANGO_EMAIL_URL']
EMAIL_RESEND_COOLDOWN = 120

if EMAIL_MODE == 'smtp':
    EMAIL_HOST = os.environ['DJANGO_EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['DJANGO_EMAIL_USER']
    EMAIL_PORT = os.environ['DJANGO_EMAIL_PORT']
    EMAIL_HOST_PASSWORD = os.environ['DJANGO_EMAIL_PASSWORD']
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
elif EMAIL_MODE == 'sendgrid':
    SENDGRID_USER = os.environ['SENDGRID_USER']

CELERY_BROKER_URL = f'amqp://{AMQP_USER}:{AMQP_PASS}@{AMQP_HOST}:{AMQP_PORT}/{AMQP_VHOST}'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_IMPORTS = [
    'api.celery_tasks',
]

GUARDIAN_RAISE_403 = True

"""
    2.5MB - 2621440
    5MB - 5242880
    10MB - 10485760
    20MB - 20971520
    50MB - 52428800
    100MB 104857600
    250MB - 214958080
    500MB - 429916160
"""
MAX_FILE_SIZE = 20971520
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520


def is_user_silk_authorized(user):
    return user.is_superuser


SILKY_PYTHON_PROFILER = False
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_PERMISSIONS = is_user_silk_authorized
SILKY_META = True

# noinspection PyUnresolvedReferences
STATIC_ROOT = '/static/'
STATIC_URL = '/static/'

ADMIN_GROUP_NAME = 'Administrators'
