import os
from ..base import BASE_DIR

# 프로젝트 최상위 디렉토리에 'media' 폴더를 만들어 파일을 관리합니다.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')