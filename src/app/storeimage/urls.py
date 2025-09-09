from django.urls import path
from . import views

urlpatterns = [
    # 예: http://127.0.0.1:8000/gallery/ 주소로 접속하면 display_crawled_images 뷰를 실행
    path('gallery/', views.display_crawled_images, name='image_gallery'),
]