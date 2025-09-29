import io
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드가 없는 환경에서 Matplotlib 사용 설정
import matplotlib.pyplot as plt

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache

def congestion_status(request):
    """현재 혼잡도 상태를 JSON으로 반환하는 API 뷰"""
    # ★★★ 전역 변수 대신 Django 캐시에서 상태 조회 ★★★
    status = cache.get('current_congestion_status', {
        "level": 0,
        "label": "측정중",
        "occupancy": 0,
        "object_count": 0
    }) # 캐시에 값이 없으면 기본값 반환
    return JsonResponse(status)


def congestion_graph_view(request):
    """캐시에 저장된 데이터를 바탕으로 통일된 y축을 사용하는 그래프 이미지를 생성하여 반환"""
    history = cache.get('congestion_history')

    if not history:
        return HttpResponse("아직 데이터가 수집되지 않았습니다.", status=204)

    timestamps, counts = zip(*history)

    # --- Matplotlib으로 그래프 생성 (수정된 버전) ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 1. 막대 그래프 (ax1에 그리기)
    ax1.bar(timestamps, counts, color='skyblue', label='Occupation')
    
    # 2. 꺾은선 그래프 (동일한 ax1에 그리기)
    ax1.plot(timestamps, counts, color='red', marker='o', linestyle='-', label='Trend')

    # Y축 라벨을 하나로 통합합니다.
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Occupation / Trend", color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.tick_params(axis='x', rotation=45)

    # 범례(legend)를 추가하여 두 그래프를 명확히 구분해 줍니다.
    ax1.legend()

    fig.suptitle('Time-based Congestion Rate')
    fig.tight_layout()

    # --- 그래프를 이미지 버퍼에 저장 ---
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    return HttpResponse(buf.getvalue(), content_type='image/png')