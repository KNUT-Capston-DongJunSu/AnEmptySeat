# your_app/views.py
import time
from django.http import StreamingHttpResponse
from django.core.cache import cache
from .stream_manager import stream_manager # 👈 1. StreamManager 인스턴스 임포트

def live_stream_view(request, file_name):
    """
    요청된 비디오의 처리 스레드를 실행(필요시)하고,
    캐시에서 프레임을 가져와 스트리밍하는 뷰.
    """
    # 👈 2. 이 뷰가 호출될 때, 해당 비디오 처리 스레드가 실행되도록 요청
    stream_manager.start_processor_if_not_running(file_name)

    # 👈 3. 기존의 프레임 생성 및 전송 로직은 그대로 유지
    def frame_generator():
        while True:
            # file_name을 사용하여 고유한 캐시 키를 조회
            cache_key = f'{file_name}_latest_frame_bytes'
            frame_bytes = cache.get(cache_key)
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # CPU 부하를 줄이기 위한 지연
            time.sleep(0.03)

    return StreamingHttpResponse(
        frame_generator(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

# congestion_status, congestion_graph_view 등 다른 뷰는 그대로 유지합니다.