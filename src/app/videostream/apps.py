from django.apps import AppConfig
import os

class VideostreamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.app.videostream'

    def ready(self):
        # Django 서버가 준비되면 백그라운드 스레드를 시작
        # 실제 운영 환경에서는 이 방식이 완벽하지 않을 수 있으므로 주의가 필요합니다.
        # (manage.py runserver는 두 번 실행될 수 있음)
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .stream_manager import StreamManager
            
            processor = StreamManager()
            processor.get_or_create_processor("111.mp4")
            print("Video processing background thread started.")