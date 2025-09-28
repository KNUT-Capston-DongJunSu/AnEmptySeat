frame_width, frame_height = 1270, 720

class CongestionCalculator:
    
    history = []

    def __init__(self, history_len=30):    
        self.history_len = history_len  # 최근 N 프레임
    
    def update_history(self, per_person_score):
        self.history.append(per_person_score)
        if len(self.history) > self.history_len:
            self.history.pop(0)
    
    def calculate_level(self, occupancy_score, num_objects):
        if num_objects == 0:
            return 1, "원활"
        
        per_person_score = occupancy_score / num_objects
        self.update_history(per_person_score)
        
        # 최근 N 프레임 최대값 기준으로 상대적 비율
        max_score = max(self.history) + 1e-6
        ratio = per_person_score / max_score
        print(f"max_score, per_person_score, self.history: {max_score} {per_person_score} {self.history}")
        if ratio <= 0.25:
            return 1, "원활"
        elif ratio <= 0.5:
            return 2, "보통"
        elif ratio <= 0.75:
            return 3, "혼잡"
        else:
            return 4, "매우 혼잡"
