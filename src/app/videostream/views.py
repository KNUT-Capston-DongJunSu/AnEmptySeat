import time
from django.core.cache import cache
from django.http import StreamingHttpResponse

def live_stream_view(request):
    # 이제 이 뷰는 프레임을 생성하지 않고, 캐시에서 가져와 전달만 합니다.
    def frame_generator():
        while True:
            frame_bytes = cache.get('latest_frame_bytes')
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # 너무 빠른 루프를 방지하기 위해 약간의 지연 시간 추가
            time.sleep(0.03) # 약 30fps에 해당

    return StreamingHttpResponse(
        frame_generator(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


