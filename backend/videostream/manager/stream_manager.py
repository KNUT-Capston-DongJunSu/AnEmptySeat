# stream_manager.py
import os, cv2, time, threading
from backend.config.settings import BASE_DIR, VIDEO_DIR, MODEL_PATH
from .video_processor import VideoProcessor 
from ..ml.yolo_manager import YoloManager

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

            print(f"Creating new processor for {file_name}")

            processor = VideoProcessor(
                file_name=file_name,
                model=YOLO_MODEL
            )
            processor.start()
            self.processors[file_name] = processor

# 애플리케이션 전체에서 사용할 단일 인스턴스
stream_manager = StreamManager()