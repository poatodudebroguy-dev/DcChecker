import cv2
import numpy as np
from ultralytics import YOLO

def is_inside(box, polygon):
    """
    Checks if the center of the detected box is inside the defined polygon (parking spot).
    """
    x1, y1, x2, y2 = box
    center_point = ((x1 + x2) / 2, (y1 + y2) / 2)
    return cv2.pointPolygonTest(np.array(polygon, np.int32), center_point, False) >= 0

# Example Map: Define your coordinates here [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
PARKING_MAP = {
    "Space A1": [(50, 100), (200, 100), (200, 300), (50, 300)],
    "Space A2": [(210, 100), (360, 100), (360, 300), (210, 300)],
    # Add more spots as needed
}

def run_parking_bot(source="parking_lot.png", parking_map=PARKING_MAP, confidence=0.45):
    """
    A bot that detects cars, motorcycles, and trucks using YOLOv8.
    It strictly ignores people (Class 0) to focus on vehicle occupancy.
    
    :param source: 0 for webcam, a video path, or an image path.
    :param parking_map: Dictionary of spot names and their polygon coordinates.
    :param confidence: Minimum confidence threshold for detection.
    """
    model = YOLO("yolov8n.pt")

    # Filter for: 2 (car), 3 (motorcycle), 7 (truck)
    TARGET_CLASSES = [2, 3, 7] 

    # Determine source type
    is_image = isinstance(source, str) and source.lower().endswith(('.png', '.jpg', '.jpeg'))
    
    if not is_image:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Error: Could not open source {source}")
            return
    else:
        cap = None

    print("--- Vehicle Detection Bot Active ---")
    print("Filtering for: Cars, Motorcycles, and Trucks.")

    while True:
        if is_image:
            frame = cv2.imread(source)
            if frame is None:
                print(f"Error: Could not find the image file: {source}")
            ret = frame is not None
        else:
            ret, frame = cap.read()

        if not ret: break

        # Perform detection
        results = model.predict(
            source=frame, 
            classes=TARGET_CLASSES, 
            conf=confidence, 
            verbose=False
        )

        # Extract detections for the current frame
        detections = results[0].boxes
        
        # Track occupancy
        occupancy_results = {name: "Free" for name in parking_map.keys()}
        
        for box_tensor in detections.xyxy:
            box = box_tensor.cpu().numpy()
            for spot_name, polygon in parking_map.items():
                if is_inside(box, polygon):
                    occupancy_results[spot_name] = "Occupied"

        # Visualize results on the frame
        annotated_frame = results[0].plot()

        # Draw the parking spot polygons
        for spot_name, polygon in parking_map.items():
            color = (0, 0, 255) if occupancy_results[spot_name] == "Occupied" else (0, 255, 0)
            pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [pts], True, color, 2)
            
            cv2.putText(annotated_frame, spot_name, (polygon[0][0], polygon[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        print(f"Status Update: {occupancy_results}")
        cv2.imshow("Parking Lot Bot", annotated_frame)

        if is_image:
            print("Analysis complete. Press any key to close window.")
            cv2.waitKey(0)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if cap: cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_parking_bot()
