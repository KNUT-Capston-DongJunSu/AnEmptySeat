import os
from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.static import static

def index_page(request):
    """VIDEO_DIR 내 mp4 파일 목록을 보여주는 랜딩 페이지"""
    video_dir = settings.VIDEO_DIR
    try:
        files = sorted(f for f in os.listdir(video_dir) if f.endswith('.mp4'))
    except FileNotFoundError:
        files = []
    return render(request, 'index.html', {'files': files})

def main_page(request, file_name):
    """메인 페이지를 렌더링하는 뷰 함수"""
    return render(request, 'project.html', {'file_name': file_name})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stream/', include('backend.videostream.urls')),
    path('project/<str:file_name>/', main_page, name='main'),
    path('', index_page, name='index'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)