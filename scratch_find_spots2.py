import cv2
import numpy as np

img = cv2.imread('IMG_0764.png', 0)

# Dilate to close gaps
kernel = np.ones((5, 5), np.uint8)
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=3)

contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

spots = []
count = 1
for cnt in contours:
    area = cv2.contourArea(cnt)
    if 20000 < area < 400000:
        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        # We look for rectangles
        if len(approx) >= 4:
            # get bounding rect or minimum area rectangle
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int32(box)
            spots.append((f"Space {count}", box.tolist()))
            count += 1

print(f"Found {len(spots)} spots.")
if spots:
    print("First spot:", spots[0])
    
# Draw and save to see if it makes sense
annotated = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for name, box in spots:
    pts = np.array(box, np.int32).reshape((-1, 1, 2))
    cv2.polylines(annotated, [pts], True, (0, 255, 0), 5)
cv2.imwrite('debug_spots.png', annotated)
