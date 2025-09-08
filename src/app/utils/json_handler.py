import os
import json

def load_json_data(json_path):
    """JSON 데이터 로드"""
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_json_data(json_path, data):
    """JSON 데이터 저장"""
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

"""
data = {
    "Progress_Logs_html": progress_logs,
    "Density_Data_html": density_data
}
"""