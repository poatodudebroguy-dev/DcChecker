import cv2
import numpy as np
import time
import json
import os

# YOLO removed: Standard YOLOv8 struggles with top-down satellite imagery (detects cars as 'toilets').
# We use a custom computer vision variance algorithm instead.

LATEST_STATUS = {}

# Example Map: Define your coordinates here [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
PARKING_MAP = {
    "Space 1": [(1131, 57), (1294, 57), (1294, 469), (1131, 469)],
    "Space 2": [(1294, 57), (1457, 57), (1457, 469), (1294, 469)],
    "Space 3": [(1457, 57), (1619, 57), (1619, 469), (1457, 469)],
    "Space 4": [(1619, 57), (1782, 57), (1782, 469), (1619, 469)],
    "Space 5": [(1782, 57), (1945, 57), (1945, 469), (1782, 469)],
    "Space 6": [(1945, 57), (2108, 57), (2108, 469), (1945, 469)],
    "Space 7": [(2108, 57), (2271, 57), (2271, 469), (2108, 469)],
    "Space 8": [(2271, 57), (2434, 57), (2434, 469), (2271, 469)],
    "Space 9": [(2434, 57), (2597, 57), (2597, 469), (2434, 469)],
    "Space 10": [(1039, 2013), (1202, 2013), (1202, 2425), (1039, 2425)],
    "Space 11": [(1202, 2013), (1364, 2013), (1364, 2425), (1202, 2425)],
    "Space 12": [(1364, 2013), (1527, 2013), (1527, 2425), (1364, 2425)],
    "Space 13": [(1527, 2013), (1690, 2013), (1690, 2425), (1527, 2425)],
    "Space 14": [(1690, 2013), (1853, 2013), (1853, 2425), (1690, 2425)],
    "Space 15": [(1853, 2013), (2016, 2013), (2016, 2425), (1853, 2425)],
    "Space 16": [(2016, 2013), (2179, 2013), (2179, 2425), (2016, 2425)],
    "Space 17": [(609, 616), (1008, 616), (1008, 775), (609, 775)],
    "Space 18": [(609, 775), (1008, 775), (1008, 933), (609, 933)],
    "Space 19": [(609, 933), (1008, 933), (1008, 1092), (609, 1092)],
    "Space 20": [(609, 1092), (1008, 1092), (1008, 1251), (609, 1251)],
    "Space 21": [(609, 1251), (1008, 1251), (1008, 1410), (609, 1410)],
    "Space 22": [(609, 1410), (1008, 1410), (1008, 1569), (609, 1569)],
    "Space 23": [(609, 1569), (1008, 1569), (1008, 1728), (609, 1728)],
    "Space 24": [(609, 1728), (1008, 1728), (1008, 1887), (609, 1887)],
    "Space 25": [(609, 1887), (1008, 1887), (1008, 2046), (609, 2046)],
    "Space 26": [(609, 2046), (1008, 2046), (1008, 2205), (609, 2205)],
    "Space 27": [(609, 2205), (1008, 2205), (1008, 2364), (609, 2364)],
    "Space 28": [(2790, 616), (3190, 616), (3190, 775), (2790, 775)],
    "Space 29": [(2790, 775), (3190, 775), (3190, 933), (2790, 933)],
    "Space 30": [(2790, 933), (3190, 933), (3190, 1092), (2790, 1092)],
    "Space 31": [(2790, 1092), (3190, 1092), (3190, 1251), (2790, 1251)],
    "Space 32": [(2790, 1251), (3190, 1251), (3190, 1410), (2790, 1410)],
    "Space 33": [(2790, 1410), (3190, 1410), (3190, 1569), (2790, 1569)],
    "Space 34": [(2790, 1569), (3190, 1569), (3190, 1728), (2790, 1728)],
    "Space 35": [(2790, 1728), (3190, 1728), (3190, 1887), (2790, 1887)],
    "Space 36": [(2790, 1887), (3190, 1887), (3190, 2046), (2790, 2046)],
    "Space 37": [(2790, 2046), (3190, 2046), (3190, 2205), (2790, 2205)],
    "Space 38": [(2790, 2205), (3190, 2205), (3190, 2364), (2790, 2364)],
    "Space 39": [(1392, 1057), (1561, 1057), (1561, 1498), (1392, 1498)],
    "Space 40": [(1561, 1057), (1730, 1057), (1730, 1498), (1561, 1498)],
    "Space 41": [(1730, 1057), (1899, 1057), (1899, 1498), (1730, 1498)],
    "Space 42": [(1899, 1057), (2068, 1057), (2068, 1498), (1899, 1498)],
    "Space 43": [(2068, 1057), (2237, 1057), (2237, 1498), (2068, 1498)],
    "Space 44": [(1392, 1498), (1561, 1498), (1561, 1940), (1392, 1940)],
    "Space 45": [(1561, 1498), (1730, 1498), (1730, 1940), (1561, 1940)],
    "Space 46": [(1730, 1498), (1899, 1498), (1899, 1940), (1730, 1940)],
    "Space 47": [(1899, 1498), (2068, 1498), (2068, 1940), (1899, 1940)],
    "Space 48": [(2068, 1498), (2237, 1498), (2237, 1940), (2068, 1940)],
}

def run_parking_bot(source="parking_lot.png", parking_map=PARKING_MAP, headless=False):
    """
    A custom computer vision bot that detects cars using pixel variance and edge density.
    This works significantly better for top-down satellite imagery than standard YOLO models.
    
    :param source: 0 for webcam, a video path, or an image path.
    :param parking_map: Dictionary of spot names and their polygon coordinates.
    :param headless: Run without popping up an OpenCV window.
    """
    # Refer to the variable at the top of this file
    global LATEST_STATUS

    # Resolve source path: if not found, check the script's directory
    if isinstance(source, str) and not os.path.isabs(source) and not os.path.exists(source):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        potential_path = os.path.join(script_dir, source)
        if os.path.exists(potential_path):
            source = potential_path
    print(f"Bot Source Path: {os.path.abspath(source)}")

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
    print("Using Custom Top-Down Variance Algorithm.")
    if not headless:
        cv2.namedWindow("Parking Lot Bot", cv2.WINDOW_NORMAL)

    while True:
        if is_image:
            frame = cv2.imread(source)
            if frame is None:
                print(f"Error: Could not find the image file: {source}")
            ret = frame is not None
        else:
            ret, frame = cap.read()

        if not ret: break

        # Track occupancy using CV variance
        occupancy_results = {name: "Free" for name in parking_map.keys()}
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        annotated_frame = frame.copy()

        for spot_name, polygon in parking_map.items():
            mask = np.zeros(gray.shape, dtype=np.uint8)
            pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
            cv2.fillPoly(mask, [pts], 255)
            
            # Calculate color variance and edge density
            mean, stddev = cv2.meanStdDev(frame, mask=mask)
            avg_std = np.mean(stddev)
            
            spot_pixels = cv2.bitwise_and(edges, edges, mask=mask)
            num_edge_pixels = np.count_nonzero(spot_pixels)
            total_pixels = np.count_nonzero(mask)
            edge_density = num_edge_pixels / total_pixels if total_pixels > 0 else 0
            
            # Optimized thresholds for satellite imagery detection
            if avg_std > 8.0 or edge_density > 0.008:
                occupancy_results[spot_name] = "Occupied"
            
            # Debug: Uncomment the line below to see the raw values for tuning
            # print(f"{spot_name} -> Variance: {avg_std:.2f}, Edges: {edge_density:.4f}")

        # Draw the parking spot polygons
        for spot_name, polygon in parking_map.items():
            is_occupied = occupancy_results[spot_name] == "Occupied"
            color = (0, 0, 255) if is_occupied else (0, 255, 0)
            pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [pts], True, color, 2)
            
            cv2.putText(annotated_frame, spot_name, (polygon[0][0], polygon[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Print summary and update global status for the Flask API
        occupied_count = list(occupancy_results.values()).count("Occupied")
        print(f"\nBot Heartbeat: {len(occupancy_results)} spots scanned. {occupied_count} occupied.")
        
        # Clear and update the global dictionary so app.py always has the latest
        LATEST_STATUS.clear()
        LATEST_STATUS.update(occupancy_results)

        if not headless:
            cv2.imshow("Parking Lot Bot", annotated_frame)

            if is_image:
                # For images, wait 5 seconds then loop (allows picking up file changes)
                if cv2.waitKey(5000) & 0xFF == ord('q'):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            # Small delay to prevent high CPU usage
            if is_image:
                time.sleep(5)
            else:
                time.sleep(1)

    if cap: cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_parking_bot()
