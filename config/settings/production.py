from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

# Core Settings
DEBUG = True  # Temporarily True for testing
SECRET_KEY = os.getenv('PROD_DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['*']  # Update with actual domain later

# Add Whitenoise configuration
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # Add after SecurityMiddleware

# Add this for better static file handling
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('PROD_DB_NAME'),
        'USER': os.getenv('PROD_DB_USER'),
        'PASSWORD': os.getenv('PROD_DB_PASSWORD'),
        'HOST': os.getenv('PROD_DB_HOST'),
        'PORT': os.getenv('PROD_DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
    }
}

# Static and Media Files Settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# For local testing, use FileSystemStorage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security Settings (disabled for testing)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CORS Settings
'''CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Keep existing frontend local
    "http://localhost:3000",  # Common React port
    
    # Production
    "https://app.cardiacsounds.cn"
]'''

# OR for testing purposes:
CORS_ALLOW_ALL_ORIGINS = True  # Simpler but less secure option

# Aliyun SMS Settings
ALIYUN_SMS = {
    'ACCESS_KEY_ID': os.getenv('ALIYUN_SMS_KEY_ID'),
    'ACCESS_KEY_SECRET': os.getenv('ALIYUN_SMS_KEY_SECRET'),
    'TEMPLATE_CODE': os.getenv('ALIYUN_SMS_TEMPLATE_CODE'),
    'SIGN_NAME': os.getenv('ALIYUN_SMS_SIGN_NAME')
}

# Comment out OSS settings for now - will enable when deploying
"""
# Aliyun OSS Settings
DEFAULT_FILE_STORAGE = 'storages.backends.aliyun_oss.AliyunOSSStorage'
STATICFILES_STORAGE = 'storages.backends.aliyun_oss.AliyunOSSStorage'
ALI_OSS_ACCESS_KEY_ID = os.getenv('ALI_OSS_ACCESS_KEY_ID')
ALI_OSS_ACCESS_KEY_SECRET = os.getenv('ALI_OSS_ACCESS_KEY_SECRET')
ALI_OSS_BUCKET_NAME = os.getenv('ALI_OSS_BUCKET_NAME')
ALI_OSS_ENDPOINT = os.getenv('ALI_OSS_ENDPOINT')
"""