from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")
frame = cv2.imread("parking_lot.png")
results = model.predict(source=frame, classes=[2, 3, 7], conf=0.45, verbose=False)

detections = results[0].boxes
print(f"Detected {len(detections.xyxy)} vehicles.")
if len(detections.xyxy) > 0:
    for i, box in enumerate(detections.xyxy[:5]):
        print(f"Box {i}: {box.cpu().numpy()}")
