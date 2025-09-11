import cv2
from django.http import StreamingHttpResponse
from .video_streaming import SingleThreadStreamer
from src.ml.utils.tracking import tracking_object
from src.ml.utils.drawing_boxes import draw_tracking_boxes


def generate_frames(video_path, model_path, camera_height):
    # BaseVideoStreamer 와 유사한 초기화 로직
    streamer = SingleThreadStreamer(video_path, model_path, "dummy_output", camera_height)

    while streamer.cap.isOpened():
        ret, frame = streamer.cap.read()
        if not ret:
            break

        # 딥러닝 처리
        results = streamer.model.smart_predict_yolo(frame=frame, conf=0.5)
        tracked_objects = tracking_object(streamer.tracker, results, streamer.frame_id)
        plot = draw_tracking_boxes(frame, tracked_objects)
        
        # 결과를 비디오 파일이 아닌 JPEG 이미지로 인코딩
        ret, buffer = cv2.imencode('.jpg', plot)
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()

        # HTTP 스트리밍 형식에 맞춰 데이터 전송 (yield)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    streamer.stop_stream()


def live_stream_view(request):
    video_path = "path/to/source_video.mp4"
    model_path = "path/to/model.pt"
    camera_height = 2.0
    
    return StreamingHttpResponse(
        generate_frames(video_path, model_path, camera_height),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
