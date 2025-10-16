from django.urls import path
from . import views

urlpatterns = [
    # 1. 기존 비디오 스트림 URL (유지)
    # 예: /stream/cctv1.mp4/
    path('stream/<str:file_name>/', views.live_stream_view, name='live_stream_view'),

    # 2. 혼잡도 데이터 API URL (추가)
    # 예: /api/status/cctv1.mp4/
    path('api/status/<str:file_name>/', views.congestion_status, name='congestion_status'),

    # 3. 그래프 이미지 API URL (추가)
    # 예: /api/graph/cctv1.mp4/
    path('api/graph/<str:file_name>/', views.congestion_graph_view, name='congestion_graph'),
    
]