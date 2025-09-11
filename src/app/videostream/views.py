import cv2
import time # 시간 기록을 위해 time 모듈 추가
from collections import deque # 리스트의 크기를 일정하게 유지하기 위해 deque 사용

from django.core.cache import cache
from django.http import StreamingHttpResponse

from .video_streaming import SingleThreadStreamer
from src.ml.utils.tracking import tracking_object
from src.ml.utils.drawing_boxes import draw_tracking_boxes
from src.app.analy.calc_congestion import calculate_congestion


# def generate_frames(video_path, model_path, camera_height):
#     # BaseVideoStreamer 와 유사한 초기화 로직
#     streamer = SingleThreadStreamer(video_path, model_path, "dummy_output", camera_height)

#     while streamer.cap.isOpened():
#         ret, frame = streamer.cap.read()
#         if not ret:
#             break

#         # 딥러닝 처리
#         results = streamer.model.smart_predict_yolo(frame=frame, conf=0.5)
#         tracked_objects = tracking_object(streamer.tracker, results, streamer.frame_id)
#         plot = draw_tracking_boxes(frame, tracked_objects)
        
#         # 결과를 비디오 파일이 아닌 JPEG 이미지로 인코딩
#         ret, buffer = cv2.imencode('.jpg', plot)
#         if not ret:
#             continue
        
#         frame_bytes = buffer.tobytes()

#         # HTTP 스트리밍 형식에 맞춰 데이터 전송 (yield)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     streamer.stop_stream()

def generate_frames(video_path, model_path, camera_height):
    streamer = SingleThreadStreamer(video_path, model_path, "dummy_output", camera_height)

    while streamer.cap.isOpened():
        ret, frame = streamer.cap.read()
        if not ret:
            # 비디오가 끝나면 처음부터 다시 시작
            streamer.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # --- 딥러닝 및 혼잡도 계산 로직 ---
        results = streamer.model.smart_predict_yolo(frame=frame, conf=0.5)
        tracked_objects = tracking_object(streamer.tracker, results, streamer.frame_id)

        ### 점유율 추정 로직 추가
        # occupancy = 
         
        level, label = calculate_congestion(occupancy)
        plot = draw_tracking_boxes(frame, tracked_objects, label)

        # ★★★ 1. 현재 상태를 캐시에 저장 (기존 로직) ★★★
        congestion_data = {"level": level, "label": label, "occupancy": occupancy}
        cache.set('current_congestion_status', congestion_data, timeout=10)

        # ★★★ 2. 5초마다 시간별 데이터를 캐시에 누적 저장 (새로운 로직) ★★★
        current_time = time.time()
        if current_time - last_update_time > 5:
            last_update_time = current_time
            
            # deque를 사용해 항상 최신 30개 데이터만 유지
            history = cache.get('congestion_history', deque(maxlen=30))
            
            # 현재 시간과 객체 수를 튜플 형태로 추가
            history.append((time.strftime('%H:%M:%S'), occupancy))
            
            # 업데이트된 내역을 다시 캐시에 저장
            cache.set('congestion_history', history, timeout=3600)

        # JPEG 이미지로 인코딩
        ret, buffer = cv2.imencode('.jpg', plot)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()

        # HTTP 스트리밍 형식에 맞춰 데이터 전송 (yield)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    streamer.cap.release()


def live_stream_view(request):
    video_path = "path/to/source_video.mp4"
    model_path = "path/to/model.pt"
    camera_height = 2.0
    
    return StreamingHttpResponse(
        generate_frames(video_path, model_path, camera_height),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

