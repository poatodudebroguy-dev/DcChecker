import cv2
import numpy as np

# Load the image
img = cv2.imread(r'c:\Users\potat\Desktop\DcChecker\IMG_0764.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image to get the outlines
# Assuming white outlines on black background or black on white
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

parking_spots = []
count = 1
for cnt in contours:
    # Approximate the contour
    epsilon = 0.05 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    
    # If it has 4 corners, it might be a parking spot
    if len(approx) == 4:
        area = cv2.contourArea(approx)
        if area > 1000: # Filter out small noise
            pts = [tuple(pt[0]) for pt in approx]
            # Convert numpy types to native Python types
            pts = [(int(x), int(y)) for x, y in pts]
            parking_spots.append((f"Space {count}", pts))
            count += 1

# If empty, maybe try different threshold
if not parking_spots:
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        epsilon = 0.05 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > 1000:
                pts = [tuple(pt[0]) for pt in approx]
                pts = [(int(x), int(y)) for x, y in pts]
                parking_spots.append((f"Space {count}", pts))
                count += 1

# Draw spots
annotated = img.copy()
for name, pts in parking_spots:
    pts_arr = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.polylines(annotated, [pts_arr], True, (0, 255, 0), 2)
    cv2.putText(annotated, name, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

cv2.imwrite(r'c:\Users\potat\Desktop\DcChecker\annotated.png', annotated)

# Output map
parking_map = {name: pts for name, pts in parking_spots}
print("PARKING_MAP =", parking_map)
