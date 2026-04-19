import cv2
import numpy as np
from ultralytics import YOLO
import json

# Load scaled map
with open('scaled_map.json', 'r') as f:
    PARKING_MAP = json.load(f)

def is_inside(box, polygon):
    x1, y1, x2, y2 = box
    center_point = ((x1 + x2) / 2, (y1 + y2) / 2)
    return cv2.pointPolygonTest(np.array(polygon, np.int32), center_point, False) >= 0

model = YOLO("yolov8n.pt")
TARGET_CLASSES = [2, 3, 7] 

frame = cv2.imread("parking_lot.png")
results = model.predict(source=frame, classes=TARGET_CLASSES, conf=0.45, verbose=False)
detections = results[0].boxes
occupancy_results = {name: "Free" for name in PARKING_MAP.keys()}

for box_tensor in detections.xyxy:
    box = box_tensor.cpu().numpy()
    for spot_name, polygon in PARKING_MAP.items():
        if is_inside(box, polygon):
            occupancy_results[spot_name] = "Occupied"

annotated_frame = results[0].plot()

for spot_name, polygon in PARKING_MAP.items():
    color = (0, 0, 255) if occupancy_results[spot_name] == "Occupied" else (0, 255, 0)
    pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
    cv2.polylines(annotated_frame, [pts], True, color, 4)
    cv2.putText(annotated_frame, spot_name, (polygon[0][0], polygon[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

# Resize to something reasonable for artifact viewing
small = cv2.resize(annotated_frame, (0,0), fx=0.3, fy=0.3)
cv2.imwrite("c:/Users/potat/.gemini/antigravity/brain/9c994b33-cdd0-47ae-9510-102df8936520/scratch/preview.png", small)
cv2.imwrite("annotated_preview.png", small)
