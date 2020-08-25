import base64
import os
from datetime import timedelta
from urllib.parse import urljoin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'h&jxpswi*y%lij@2i)8cv^eq4r3ro2%+(9cw9in+h9e4vd6#zi'
DEBUG = True

AUTH_USER_MODEL = "users.User"
ALLOWED_HOSTS = ["*"]
USE_X_FORWARDED_HOST = True

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "corsheaders",
    "phonenumber_field",
]

LOCAL_APPS = [
    "apps.authentication.apps.AuthenticationConfig",
    "apps.products.apps.ProductsConfig",
    "apps.website.apps.WebsiteConfig",
    "apps.clubs.apps.ClubsConfig",
    "apps.person.apps.PersonConfig",
    "apps.core.apps.CoreConfig",
    "apps.users.apps.UsersConfig",
    "apps.grades.apps.GradesConfig",
    "apps.sms.apps.SmsConfig",
    "apps.subscriptions.apps.SubscriptionsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uniclub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'uniclub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "uniclub"),
        "USER": os.getenv("DB_USER", "uniclub"),
        "PASSWORD": os.getenv("DB_PASSWORD", "uniclub"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DEEP_LINKING": True,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROSETTA_UWSGI_AUTO_RELOAD = True
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_EXCLUDED_APPLICATIONS = (
    "django",
    "django_extensions",
    "phonenumber_field",
    "rosetta",
)


# Celery settings
CELERY_BROKER_URL = "pyamqp://{user}:{pwd}@{host}:{port}/{vhost}".format(
    user=os.getenv("RABBIT_USER", "guest"),
    pwd=os.getenv("RABBIT_PASSWORD", "guest"),
    host=os.getenv("RABBIT_HOST", "localhost"),
    port=os.getenv("RABBIT_PORT", "5672"),
    vhost=os.getenv("RABBIT_VHOST", "/"),
)
CELERY_RESULT_BACKEND = "redis://{host}:{port}/{db_index}".format(
    host=os.getenv("CELERY_REDIS_HOST", "localhost"),
    port=os.getenv("CELERY_REDIS_PORT", "6379"),
    db_index=os.getenv("CELERY_REDIS_DB_INDEX", "0"),
)
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERY_RESULT_EXTENDED = False
CELERY_RESULT_EXPIRES = 3600
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False
CELERY_TASK_TRACK_STARTED = True


DEBUG_TOOLBAR_ENABLED = os.getenv("DEBUG_TOOLBAR_ENABLED", True)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {"django.db.backends": {"handlers": ["console"], "level": "INFO"}},
}

HOTP_KEY = base64.b32encode(SECRET_KEY.encode("utf-8"))

# SMS
KAZINFO_URL = 'http://kazinfoteh.org:9507/api'
KAZINFO_USERNAME = os.environ.get('KAZ_INFO_USERNAME', 'juniklab1')
KAZINFO_PASSWORD = os.environ.get('KAZ_INFO_PASSWORD', 'jdDZ1NcK1')

# OTP settings
OTP_LENGTH = 4
OTP_VALIDITY_PERIOD = 120  # in minutes
