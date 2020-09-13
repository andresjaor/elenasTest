import os
from configurations import Configuration
from pathlib import Path
from django.urls import reverse_lazy


class Common(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = 'gx2f=prncgcz!#p_o8u0t=1s%+_l7oj+(u=2s)w7u5z5&$+)(t'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        'task_manager.apps.TaskManagerConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework.authtoken'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'elenas.urls'

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 9,
            }
        }
    ]

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

    WSGI_APPLICATION = 'elenas.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    TASKS_PER_PAGE = 10

    AUTH_USER_MODEL = 'auth.User'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication'
        ]
    }


class Dev(Common):
    SECRET_KEY = os.getenv('SECRET_KEY', Common.SECRET_KEY)


class Stg(Common):
    SECRET_KEY = os.getenv('SECRET_KEY', Common.SECRET_KEY)


class Prd(Common):
    SECRET_KEY = os.getenv('SECRET_KEY', Common.SECRET_KEY)
