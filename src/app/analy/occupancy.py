W_i = 0.85
frame_width, frame_height = 640, 580

A_ROI = frame_width * frame_height

A_list = []

def calc_occupancy(W_i, A_i, A_i_p):

    # A_i_p이나 A_ROI가 0이면, 나눗셈 불가능하므로 점유율을 0으로 설정
    if A_i_p == 0 or A_ROI == 0:
        return 0.0  
    
    # head bbox 중 ROI와 겹치는 비율 
    ratio = A_i / A_i_p

    # ROI 전체 면적 대비 실제 겹치는 면적 비율 
    overlap = A_i / A_ROI

    # 점유율 계산 -> 1.0을 넘으면 1.0 값을 사용, 1.0을 넘지 않으면 기존 값 사용하는 계산 코드 설정
    S_i = min(W_i * ratio, 1.0) * overlap # W_i : confidence score (신뢰도 값)

    return S_i # 최종 점유율 반환

def total_occupancy(A_list, A_p_list):
    # 점유율 총합을 저장할 변수 초기화
    total_score = 0.0

    # 총 객체 개수 (리스트 길이로 계산)
    num_objects = len(A_list)

    # 각 객체마다 점유율 계산 반복
    for i in range(num_objects):
        # i번째 객체의 점유율 S_i 계산
        S_i = calc_occupancy(W_i, A_list[i], A_p_list[i])

        # 계산된 점유율을 총합에 더함
        total_score += S_i

    # 객체가 없을 경우 평균 계산 불가 → 0 반환
    if num_objects == 0:
        return 0.0

    # 전체 점유율 합을 객체 수로 나눠서 평균 계산
    average_score = total_score / num_objects

    # 평균 점유율 반환
    return average_score

def calc_object_area(x1, y1, x2, y2):
    X1 = x1*frame_width
    X2 = x2*frame_width
    Y1 = y1*frame_height
    Y2 = y2*frame_height

    return (X2 - X1) * (Y2 - Y1)

def total_objects_area(tracked_objects):    
    for obj in tracked_objects:
        A_list.append(calc_object_area(obj[0], obj[1], obj[2], obj[3]))

    A_p_list = A_list.copy()

    return A_list, A_p_list