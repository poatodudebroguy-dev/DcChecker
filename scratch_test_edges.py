import cv2
import numpy as np
import json

with open('scaled_map.json', 'r') as f:
    PARKING_MAP = json.load(f)

img = cv2.imread('parking_lot.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

for spot_name, polygon in list(PARKING_MAP.items())[:10]:
    # Create mask for this polygon
    mask = np.zeros(gray.shape, dtype=np.uint8)
    pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(mask, [pts], 255)
    
    # Check edge density
    spot_pixels = cv2.bitwise_and(edges, edges, mask=mask)
    num_edge_pixels = np.count_nonzero(spot_pixels)
    total_pixels = np.count_nonzero(mask)
    density = num_edge_pixels / total_pixels if total_pixels > 0 else 0
    
    print(f"{spot_name}: Edge density = {density:.4f}")
