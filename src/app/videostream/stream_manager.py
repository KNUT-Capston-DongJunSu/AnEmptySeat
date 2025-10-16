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
        self.processors = {}
        self.lock = threading.Lock()

    def start_processor_if_not_running(self, file_name):
        with self.lock:
            if file_name in self.processors and self.processors[file_name].is_alive():
                # 이미 실행 중이면 아무것도 하지 않음
                return

            print(f"Starting a new processor for '{file_name}'...")
            video_path = f"media/videos/{file_name}" # 👈 실제 영상 경로 설정

            processor = VideoProcessor(
                file_name=file_name,
                video_path=video_path,
                model=YOLO_MODEL, # 👈 미리 로드된 모델 객체 전달
                camera_height=1080
            )
            processor.start()
            self.processors[file_name] = processor

# 애플리케이션 전체에서 사용할 단일 인스턴스    
stream_manager = StreamManager()