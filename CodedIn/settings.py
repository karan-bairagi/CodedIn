
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY=os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = BASE_DIR / 'staticfiles'
INSTALLED_APPS = [
    'daphne',
    'channels',
    'corsheaders',
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'chat',
    'app',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'CodedIn.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

ASGI_APPLICATION = 'CodedIn.asgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'PASSWORD':os.environ.get('DB_PASSWORD'),
        'HOST':os.environ.get('DB_HOST'),
        'USER':os.environ.get('DB_USER'),
        'PORT':os.environ.get('DB_PORT'),
        'CONN_MAX_AGE': 60,
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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = False




STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SESSION_COOKIE_AGE = 2592000
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUD_API_KEY'),
    'API_SECRET': os.environ.get('CLOUD_API_SECRET')
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
import os
import urllib.parse
REDIS_URL = os.environ.get("REDIS_URL")

if REDIS_URL:
    url = urllib.parse.urlparse(REDIS_URL)
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [{
                    "host": url.hostname,
                    "port": url.port or 6379,
                    "password": url.password,
                    "username": url.username if url.password else None,
                }],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }
