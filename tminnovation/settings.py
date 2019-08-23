"""
Django settings for tminnovation project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTH_USER_MODEL = 'tramino.User'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# ログイン後トップページにリダイレクト
LOGIN_REDIRECT_URL = '/tramino/mypage'
LOGOUT_REDIRECT_URL = '/tramino/index'
LOGIN_URL = 'tramino:login'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z6x-p23!lbi5o+v%tt3bd4_nn-@!!u*sj8njcmww9v+v&e04%v'

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tramino',
    'gunicorn',
    'django_cleanup',
    'imagekit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tminnovation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'tminnovation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
     # 'default': {
     # 'ENGINE': 'django.db.backends.sqlite3',
     # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     # }
       'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'gradedb',
       'USER': 'shunsuke',
       'PASSWORD': 'shun0210',
       'HOST': '127.0.0.1',
       'POST': '5432',
     }
}

CACHES = {
'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'redis://localhost:6379/',
    'OPTIONS': {
        'CLIENT_CLASS': 'django_redis.client.DefaultClient'
    }
}
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'tramino.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

##############################

import dj_database_url
DATABASES['default'] = dj_database_url.config()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# ALLOWED_HOSTS = ['*']



STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'
# STATIC_URL = STATIC_ROOT

DEBUG = False


try:
    import local_settings
    DATABASES = local_settings.databases
    DEBUG = local_settings.debug
    ALLOWED_HOSTS = local_settings.allowed_hosts
except:
    pass

AWS_ACCESS_KEY_ID = 'AKIAUNTYA6OXS3ODQIGJ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tminnovation-tramino'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1日はそのキャッシュを使う
}


# 静的ファイルの設定
AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


# メディアファイルの設定。今回は「project」というプロジェクト名の例
DEFAULT_FILE_STORAGE = 'tminnovation.backends.MediaStorage'