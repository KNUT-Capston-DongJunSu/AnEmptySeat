from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/congestion/', views.congestion_api, name='congestion_api'),
     path('api/congestion_graph/', views.congestion_graph_view, name='congestion_graph'), # 이 줄 추가
]