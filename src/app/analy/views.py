# streaming_app/views.py
import cv2
import random
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.core.cache import cache

# --- 헬퍼 함수 ---
def calculate_congestion(object_count):
    """객체 수를 기반으로 혼잡도 레벨과 라벨을 반환"""
    if object_count <= 10:
        return 1, "원활"
    elif object_count <= 25:
        return 2, "보통"
    elif object_count <= 40:
        return 3, "혼잡"
    else:
        return 4, "매우 혼잡"

# --- 스트리밍 로직 ---

# --- Django 뷰 함수 ---
def index(request):
    """비디오 스트리밍을 보여줄 기본 페이지 렌더링"""
    return render(request, 'streaming_app/index.html')


def congestion_api(request):
    """현재 혼잡도 상태를 JSON으로 반환하는 API 뷰"""
    # ★★★ 전역 변수 대신 Django 캐시에서 상태 조회 ★★★
    status = cache.get('current_congestion_status', {
        "level": 0,
        "label": "측정중",
        "object_count": 0
    }) # 캐시에 값이 없으면 기본값 반환
    return JsonResponse(status)