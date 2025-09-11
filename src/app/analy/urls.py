from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/congestion/', views.congestion_api, name='congestion_api'),
]