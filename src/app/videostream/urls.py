from django.urls import path
from . import views

urlpatterns = [
    # 예: /video/stream/my_video.mp4/
    path('stream/<str:file_name>/', views.stream_video, name='stream_video'),
]