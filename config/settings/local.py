from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_HOSTS = ['*']
DEBUG = True
SECRET_KEY = 'your-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'er_triage_system',
        'USER': 'root',
        'PASSWORD': 'Juliefang7',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CORS_ALLOW_ALL_ORIGINS = True

ALIYUN_SMS = {
    'ACCESS_KEY_ID': os.getenv('ALIYUN_SMS_KEY_ID', 'your_key_id'),
    'ACCESS_KEY_SECRET': os.getenv('ALIYUN_SMS_KEY_SECRET', 'your_key_secret'),
    'TEMPLATE_CODE': os.getenv('ALIYUN_SMS_TEMPLATE_CODE', 'SMS_123456789'),
    'SIGN_NAME': os.getenv('ALIYUN_SMS_SIGN_NAME', '您的签名')
}