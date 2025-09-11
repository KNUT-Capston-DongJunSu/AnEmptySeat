import io
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드가 없는 환경에서 Matplotlib 사용 설정
import matplotlib.pyplot as plt

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache

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


def congestion_graph_view(request):
    """캐시에 저장된 데이터를 바탕으로 막대/꺾은선 그래프 이미지를 생성하여 반환"""
    history = cache.get('congestion_history')

    # 데이터가 없으면 빈 이미지나 메시지를 반환할 수 있음
    if not history:
        return HttpResponse("아직 데이터가 수집되지 않았습니다.", status=204)

    # 데이터 분리: history에서 시간과 객체 수를 각각의 리스트로 만듦
    timestamps, counts = zip(*history)

    # --- Matplotlib으로 그래프 생성 ---
    fig, ax1 = plt.subplots(figsize=(10, 6)) # 그래프 크기 지정

    # 1. 막대 그래프 (Bar Chart)
    ax1.bar(timestamps, counts, color='skyblue', label='Occupancy (Bar)')
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Occupation Ratio", color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax1.tick_params(axis='x', rotation=45) # x축 라벨 45도 회전

    # 2. 꺾은선 그래프 (Line Chart) - y축을 공유
    ax2 = ax1.twinx() # x축을 공유하는 두 번째 y축 생성
    ax2.plot(timestamps, counts, color='red', marker='o', linestyle='-', label='Occupancy (Line)')
    ax2.set_ylabel("Trend", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.suptitle('Time-based Congestion Rate')
    fig.tight_layout() # 그래프 요소들이 겹치지 않게 자동 조정

    # --- 그래프를 이미지 파일 대신 메모리 버퍼에 저장 ---
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)  # 메모리 누수 방지를 위해 그래프 객체를 닫아줌
    buf.seek(0)

    # 메모리 버퍼에 저장된 이미지 데이터를 HttpResponse로 반환
    return HttpResponse(buf.getvalue(), content_type='image/png')