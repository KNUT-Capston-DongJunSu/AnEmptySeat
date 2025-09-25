from django.urls import path
from . import views

urlpatterns = [
    # 예: /video/stream/my_video.mp4/
    path('stream/<str:file_name>/', views.live_stream_view, name='live_stream_view'),
]