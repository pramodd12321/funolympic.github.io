"""
Django settings for funolympicGame project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9)8*2nx^dz#&dfw30vt*@!l@ctaz78@6!&lskrc8-jmb6nn70o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['funolympicgame.herokuapp.com']

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "olympic",
    "notification_app",
    "channels",
    "django_celery_beat",
    "django_celery_results",

    'captcha',
    'django_password_validators',
    'django_password_validators.password_history',
    'phonenumber_field',
    'crispy_forms',
    'django_social_share',
    # 'social_django',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'social_django.middleware.SocialAuthExceptionMiddleware',

]


ROOT_URLCONF = "funolympicGame.urls"

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

                "olympic.custom_context_processors.notifications",

                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",

            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',

    'django.contrib.auth.backends.ModelBackend',

   
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',


)




WSGI_APPLICATION = "funolympicGame.wsgi.application"
ASGI_APPLICATION = 'funolympicGame.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django_password_validators.password_history.password_validation.UniquePasswordsValidator',
        'OPTIONS': {
           
             # Default: 0 - All passwords entered by the user. All password hashes are stored.
            'last_passwords': 5 # Only the last 5 passwords entered by the user
        }
    },

    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 1,
             'min_length_alpha': 2,
             'min_length_special': 1,
             'min_length_lower': 2,
             'min_length_upper': 1,
             'special_characters': "~!@#$%^&*()_+{}\":;'[]"
         }
    },

    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            'OPTIONS': {
                'user_attributes':(
                    'username', 'email', 'first_name', 'last_name'
                ),
                'max_similarity': 0.5
            }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 12,
            }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CHANNEL_LAYERS = {
    'default': {
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    },
}

# CELERY SETTINGS
CELERY_BROKER_URL =  "127.0.0.1:6379" #'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SELERLIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kathmandu'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATIC_URL = '/static/'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static/')
]


MEDIA_ROOT= os.path.join(BASE_DIR, 'media/')
MEDIA_URL= "/media/"

RECAPTCHA_PUBLIC_KEY = '6LeyOs4iAAAAAMH9ugga5_J13uXVpSz-dcLCGK-3'
RECAPTCHA_PRIVATE_KEY = '6LeyOs4iAAAAAPwAnNcuVCG783gzNiteYjl22Wmu'

RECAPTCHA_REQUIRED_SCORE = 0.85

LOGIN_REDIRECT_URL = 'dashboard'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'rijalpramodd@gmail.com' # Enter your email here
EMAIL_HOST_PASSWORD = 'xlotlntarnavpanm'   # Enter your google app token here


SOCIAL_AUTH_FACEBOOK_KEY = '2034648846723215'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '5ae83ade03b6a8162fc58f734c820bdd'  # App Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '405900337679-0u5inkfsmothejbl72lin7h4uvg1r73m.apps.googleusercontent.com'  # App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # App Secret

# django_heroku.settings(locals())


