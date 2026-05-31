"""
Django settings for lostandfound project (optimized for Render deployment).
"""

from pathlib import Path
from decouple import config
import os

VERSION = '1.0.1'

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY')  # Set in Render environment variables
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your apps
    'accounts',
    'items',
    'claims',
]

# Middleware
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

ROOT_URLCONF = 'lostandfound.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'lostandfound.wsgi.application'

# Database
DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ('developer', BASE_DIR / 'developer'),
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------------------------
# Cloud media storage (production)
# ---------------------------------------------------------------------------
# On Render (or any host where DEBUG=False), Django does NOT serve MEDIA files.
# Options:
#   1. Use Cloudinary: pip install cloudinary django-cloudinary-storage
#      Then set DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
#      and add CLOUDINARY_STORAGE = {'CLOUD_NAME': ..., 'API_KEY': ..., 'API_SECRET': ...}
#   2. Use AWS S3: pip install boto3 django-storages
#      Then set DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Set CLOUD_MEDIA = True in your .env to activate (example below uses Cloudinary).
CLOUD_MEDIA = config('CLOUD_MEDIA', default=False, cast=bool)
if CLOUD_MEDIA:
    DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE', default='cloudinary_storage.storage.MediaCloudinaryStorage')
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
        'API_KEY': config('CLOUDINARY_API_KEY', default=''),
        'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
    }

# Custom User model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Login/Logout
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'home'

# School verification code for instant account creation (set in .env)
SCHOOL_VERIFICATION_CODE = config('SCHOOL_VERIFICATION_CODE', default='SCHOOL2024')

# ---------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------
# Set EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend' in production.
# During development, 'django.core.mail.backends.console.EmailBackend' prints
# emails to the terminal instead of sending them — great for testing.
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Lost & Found <noreply@school.edu>')

# Password reset token expiry (in seconds). Default: 3600 = 1 hour.
PASSWORD_RESET_TIMEOUT = 3600