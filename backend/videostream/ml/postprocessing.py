import torch, cv2, numpy as np

# BGR 값
_BBOX_PRESETS = {
    "hotpink": (180, 105, 255),
    "yellow":  (0, 255, 255),
}

def process_predicted_results(result):
    boxes = result.boxes.xyxy
    confidences = result.boxes.conf
    classes = result.boxes.cls

    if isinstance(boxes, torch.Tensor): boxes = boxes.tolist()
    if isinstance(confidences, torch.Tensor): confidences = confidences.tolist()
    if isinstance(classes, torch.Tensor): classes = classes.tolist()
    
    data_list = [box + [conf, cls] for box, conf, cls in zip(boxes, confidences, classes)]
    results = torch.tensor(data_list, dtype=torch.float32)
    return results

def draw_tracking_boxes(frame, tracked_objects, status, trail=None, bbox_color=None, show_status=True):
    """Bounding box와 트래킹 ID 표시

    bbox_color:  None(ID별 HSV 자동), 'hotpink', 'yellow'
    show_status: True면 좌하단 인원/상태 텍스트 표시
    """
    if len(tracked_objects) == 0:
        return frame

    preset = _BBOX_PRESETS.get(bbox_color) if bbox_color else None

    original_img = frame.copy()
    height, width = original_img.shape[:2]

    for obj in tracked_objects:
        x1, y1, x2, y2, track_id = map(int, obj[:5])

        if preset is not None:
            color = preset
        else:
            hue = (track_id * 37) % 180
            color = cv2.cvtColor(np.uint8([[[hue, 255, 200]]]), cv2.COLOR_HSV2BGR)[0][0].tolist()

        if trail is not None:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            trail[track_id].append((cx, cy))
            pts = list(trail[track_id])
            for i in range(1, len(pts)):
                cv2.line(original_img, pts[i-1], pts[i], (255, 255, 0), 3)

        cv2.rectangle(original_img, (x1, y1), (x2, y2), color=color, thickness=2)
        cv2.putText(original_img, f"ID: {track_id}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)

    if show_status:
        scale = width / 1280
        thickness = max(1, round(scale * 2))
        margin = round(width * 0.02)
        text = f"{len(tracked_objects)} people | Status: {status}"
        pos = (margin, height - margin)
        # 검정 외곽선 먼저, 흰색 텍스트 위에 덮어 항상 가시성 확보
        cv2.putText(original_img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness + 3)
        cv2.putText(original_img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), thickness)

    return original_img


def draw_proximity_lines(frame, tracked_objects):
    """모든 객체 쌍을 선으로 연결 — 가까울수록 빨강, 멀수록 초록"""
    if len(tracked_objects) < 2:
        return frame

    centers = [
        ((int(obj[0]) + int(obj[2])) // 2, (int(obj[1]) + int(obj[3])) // 2)
        for obj in tracked_objects
    ]

    overlay = frame.copy()
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            cv2.line(overlay, centers[i], centers[j], (255, 255, 0), 3)

    # 선 불투명도 (1.0이면 완전 불투명)
    return cv2.addWeighted(overlay, 0.9, frame, 0.1, 0)