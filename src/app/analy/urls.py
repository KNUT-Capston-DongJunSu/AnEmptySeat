from django.urls import path
from . import views

urlpatterns = [
    path('api/congestion/', views.congestion_status, name='congestion_status'),
    path('api/congestion_graph/', views.congestion_graph_view, name='congestion_graph'), # 이 줄 추가
]