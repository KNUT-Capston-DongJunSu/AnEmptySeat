current_congestion_status = {
    "level": 1,
    "label": "원활",
    "occupancy": 0
}

def calculate_congestion(occupancy):
    """객체 수를 기반으로 혼잡도 레벨과 라벨을 반환"""
    if occupancy <= 25:
        return 1, "원활"
    elif occupancy <= 50:
        return 2, "보통"
    elif occupancy <= 75:
        return 3, "혼잡"
    else:
        return 4, "매우 혼잡"
