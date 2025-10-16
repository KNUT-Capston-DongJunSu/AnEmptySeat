import os
import threading
from django.conf import settings
from .video_streaming import VideoProcessor # VideoProcessor 클래스를 별도 파일로 분리
from src.config.settings import BASE_DIR
from src.ml.yolo_manager import YoloManager

MODEL_PATH = os.path.join(BASE_DIR, 'src', 'ml', 'weights', 'medium.pt')
YOLO_MODEL = YoloManager(MODEL_PATH)

class StreamManager:
    def __init__(self):
        self.processors = {}  # { 'video_name': VideoProcessor_instance }
        self.lock = threading.Lock() # 스레드 생성/삭제 시 동시성 제어를 위한 락

    def get_or_create_processor(self, video_name):
        with self.lock:
            if video_name not in self.processors:
                print(f"Creating new processor for {video_name}")
                video_path = os.path.join(BASE_DIR, 'front', video_name)
                if not os.path.exists(video_path):
                    return None
                
                # 2. 미리 로드된 모델 객체와 고유한 캐시 키 접두사를 전달
                processor = VideoProcessor(
                    video_path=video_path,
                    model=YOLO_MODEL, # 공유 모델 객체 전달
                    camera_height=2.0
                )
                processor.start()
                self.processors[video_name] = processor
            
            return self.processors[video_name]

# Django 앱 전체에서 공유될 단일 매니저 인스턴스
stream_manager = StreamManager()