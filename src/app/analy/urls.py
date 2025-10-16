from django.urls import path
from . import views

urlpatterns = [
    # 2. 혼잡도 데이터 API URL (추가)
    # 예: /api/status/cctv1.mp4/
    path('api/status/<str:file_name>/', views.congestion_status, name='congestion_status'),

    # 3. 그래프 이미지 API URL (추가)
    # 예: /api/graph/cctv1.mp4/
    path('api/graph/<str:file_name>/', views.congestion_graph_view, name='congestion_graph'),
]