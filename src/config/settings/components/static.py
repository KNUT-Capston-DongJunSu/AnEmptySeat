import os
from ..base import BASE_DIR

static_dir_path = os.path.join(BASE_DIR, 'front', 'static')
file_path = os.path.join(static_dir_path, 'project.css')

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    static_dir_path,
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')