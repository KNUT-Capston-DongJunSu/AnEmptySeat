import os
import cv2
import time
import threading
from collections import deque # 리스트의 크기를 일정하게 유지하기 위해 deque 사용
from ocsort import OCSort
from django.core.cache import cache
from src.ml.utils.tracking import tracking_object
from src.ml.utils.drawing_boxes import draw_tracking_boxes
from src.app.analy.occupancy import calc_spatial_density
from src.app.analy.calc_congestion import CongestionCalculator

class BaseVideoWriter:
    def __init__(self):
        self._writer = None
        self._fps = 30

    @property
    def fps(self):
        return self._fps
    
    @fps.setter
    def fps(self, value):
        self._fps = value
    
    def init_writer(self, width, height, filename):
        if self._writer is None:
            self._writer = cv2.VideoWriter(
                filename, 
                cv2.VideoWriter_fourcc(*'mp4v'), 
                self._fps, (width, height)
                )
            
        return self._writer
    
    def write(self, frame):
        return self._writer.write(frame)
    
    def close_writer(self):
        if self._writer:
            self._writer.release()
        cv2.destroyAllWindows() 
            
class BaseVideoCap:
    def __init__(self):
        self._capture = None

    def init_cap(self, video_path):
        if self._capture is None:
            self._capture = cv2.VideoCapture(video_path)
            if not self._capture.isOpened():
                raise IOError(f"Cannot open video: {video_path}")
            fps = int(self._capture.get(cv2.CAP_PROP_FPS))
            frame_width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
            frame_height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return self._capture, fps, frame_width, frame_height
    
    def close_cap(self):
        self._capture.release()
        cv2.destroyAllWindows()

class BaseVideoStreamer:
    
    scale = 1
    output_dir = "./results/predict/"
    os.makedirs(output_dir, exist_ok=True)
    resize_width = 960
    resize_height = 540

    def __init__(self, video_path, model, output_name, camera_height):
        self.frame_id = 0
        self.track_hist = []

        self.video_cap = BaseVideoCap()
        self.cap, video_fps, frame_width, frame_height = self.video_cap.init_cap(video_path)

        self.video_writer = BaseVideoWriter()
        self.video_writer.fps = video_fps
        self.video_writer.init_writer(frame_width, frame_height, self.output_dir + output_name)

        self.tracker = OCSort(det_thresh=0.3, max_age=50, min_hits=1)
        self.model = model
        # self.plotter = LivePlotter()
        # self.estimator = DensityEstimator(camera_height, frame_height)
    

class VideoProcessor(threading.Thread):
    """
    하나의 비디오 스트림을 독립적으로 처리하는 스레드 클래스입니다.
    각 인스턴스는 고유한 캐시 키를 사용하여 다른 스트림과 데이터가 섞이지 않도록 합니다.
    """
    def __init__(self, video_path, model, camera_height, cache_key_prefix):
        super().__init__()
        self.daemon = True  # 메인 스레드 종료 시 함께 종료
        self.cache_key_prefix = cache_key_prefix
        self.history_lock = threading.Lock()  # history 데이터 업데이트 시 경쟁 조건 방지를 위한 락
        self.congestion_calc = CongestionCalculator()

        # SingleThreadStreamer 초기화 시, 미리 로드된 model 객체를 전달합니다.
        # (만약 SingleThreadStreamer가 모델 경로만 받도록 되어 있다면, 
        # model 객체를 받도록 해당 클래스를 수정해야 합니다.)
        self.streamer = BaseVideoStreamer(video_path, model, "dummy_output.mp4", camera_height)

    def run(self):
        """스레드가 시작되면 실행되는 메인 영상 처리 루프입니다."""
        last_update_time = 0
        frame_id = 0
        
        # 2. 고유 캐시 키 사용: 모든 캐시 키에 접두사를 붙여 고유하게 만듭니다.
        frame_cache_key = f'{self.cache_key_prefix}_frame'
        status_cache_key = f'{self.cache_key_prefix}_status'
        history_cache_key = f'{self.cache_key_prefix}_history'

        while self.streamer.cap.isOpened():
            ret, frame = self.streamer.cap.read()
            frame_id += 1
            if frame_id % 3 != 0:
                continue
            
            if not ret:
                self.streamer.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # --- 딥러닝 및 혼잡도 계산 로직 ---
            results = self.streamer.model.smart_predict_yolo(frame=frame, conf=0.07)
            tracked_objects = tracking_object(self.streamer.tracker, results, self.streamer.frame_id)
            object_count = len(tracked_objects)

            occupancy = calc_spatial_density(tracked_objects)
            level, label = self.congestion_calc.calculate_level(occupancy, object_count)
            
            print(f"[{self.cache_key_prefix}] Occupancy: {occupancy:.2f}, Label: {label}")
            plot = draw_tracking_boxes(frame, tracked_objects, label)
            
            # JPEG 이미지로 인코딩
            ret, buffer = cv2.imencode('.jpg', plot)
            if ret:
                frame_bytes = buffer.tobytes()
                # 처리된 최종 프레임을 고유 캐시 키에 저장
                cache.set(frame_cache_key, frame_bytes, timeout=5)

            # 혼잡도 데이터를 고유 캐시 키에 저장
            congestion_data = {"level": level, "label": label, "occupancy": occupancy, "object_count": object_count}
            cache.set(status_cache_key, congestion_data, timeout=10)

            # --- 시간별 데이터 누적 저장 ---
            current_time = time.time()
            if current_time - last_update_time >= 1: # 1초마다 업데이트
                last_update_time = current_time
                
                # 3. Lock을 사용한 경쟁 조건 방지
                with self.history_lock:
                    history = cache.get(history_cache_key, deque(maxlen=30))
                    history.append((time.strftime('%H:%M:%S'), occupancy))
                    cache.set(history_cache_key, history, timeout=3600)

        self.streamer.cap.release()