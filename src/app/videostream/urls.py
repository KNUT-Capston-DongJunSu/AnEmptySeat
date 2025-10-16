from django.urls import path
from . import views

urlpatterns = [
    # 1. 기존 비디오 스트림 URL (유지)
    # 예: /stream/cctv1.mp4/
    path('stream/<str:file_name>/', views.live_stream_view, name='live_stream_view'),
]