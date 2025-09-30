from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parents[3]
SECRET_KEY = config('SECRET_KEY')
DEBUG = True

from .components.apps import *           
from .components.middleware import *     
from .components.cors_csrf import *
from .components.logging import *
from .components.templates import *
from .components.static import *

ROOT_URLCONF = "Ssrc.config.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
WSGI_APPLICATION = "Ssrc.config.wsgi.application"
ASGI_APPLICATION = "Ssrc.config.asgi.application"
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake', # 아무 이름이나 지정
    }
}