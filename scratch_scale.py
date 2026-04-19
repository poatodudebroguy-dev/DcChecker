import cv2
import numpy as np
import json

img = cv2.imread('IMG_0764.png', 0)
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Find all white pixel coordinates
points = np.column_stack(np.where(thresh > 0))

print("White pixels:", len(points))

# Let's apply the rough scaling to the PARKING_MAP and draw it to see how close it is.
# Then we can do local snapping.
PARKING_MAP = {
    "Space 1": [(375, 45), (428, 45), (428, 185), (375, 185)],
    "Space 2": [(428, 45), (481, 45), (481, 185), (428, 185)],
    "Space 3": [(481, 45), (534, 45), (534, 185), (481, 185)],
    "Space 4": [(534, 45), (587, 45), (587, 185), (534, 185)],
    "Space 5": [(587, 45), (640, 45), (640, 185), (587, 185)],
    "Space 6": [(640, 45), (693, 45), (693, 185), (640, 185)],
    "Space 7": [(693, 45), (746, 45), (746, 185), (693, 185)],
    "Space 8": [(746, 45), (799, 45), (799, 185), (746, 185)],
    "Space 9": [(799, 45), (852, 45), (852, 185), (799, 185)],
    "Space 10": [(345, 710), (398, 710), (398, 850), (345, 850)],
    "Space 11": [(398, 710), (451, 710), (451, 850), (398, 850)],
    "Space 12": [(451, 710), (504, 710), (504, 850), (451, 850)],
    "Space 13": [(504, 710), (557, 710), (557, 850), (504, 850)],
    "Space 14": [(557, 710), (610, 710), (610, 850), (557, 850)],
    "Space 15": [(610, 710), (663, 710), (663, 850), (610, 850)],
    "Space 16": [(663, 710), (716, 710), (716, 850), (663, 850)],
    "Space 17": [(205, 235), (335, 235), (335, 289), (205, 289)],
    "Space 18": [(205, 289), (335, 289), (335, 343), (205, 343)],
    "Space 19": [(205, 343), (335, 343), (335, 397), (205, 397)],
    "Space 20": [(205, 397), (335, 397), (335, 451), (205, 451)],
    "Space 21": [(205, 451), (335, 451), (335, 505), (205, 505)],
    "Space 22": [(205, 505), (335, 505), (335, 559), (205, 559)],
    "Space 23": [(205, 559), (335, 559), (335, 613), (205, 613)],
    "Space 24": [(205, 613), (335, 613), (335, 667), (205, 667)],
    "Space 25": [(205, 667), (335, 667), (335, 721), (205, 721)],
    "Space 26": [(205, 721), (335, 721), (335, 775), (205, 775)],
    "Space 27": [(205, 775), (335, 775), (335, 829), (205, 829)],
    "Space 28": [(915, 235), (1045, 235), (1045, 289), (915, 289)],
    "Space 29": [(915, 289), (1045, 289), (1045, 343), (915, 343)],
    "Space 30": [(915, 343), (1045, 343), (1045, 397), (915, 397)],
    "Space 31": [(915, 397), (1045, 397), (1045, 451), (915, 451)],
    "Space 32": [(915, 451), (1045, 451), (1045, 505), (915, 505)],
    "Space 33": [(915, 505), (1045, 505), (1045, 559), (915, 559)],
    "Space 34": [(915, 559), (1045, 559), (1045, 613), (915, 613)],
    "Space 35": [(915, 613), (1045, 613), (1045, 667), (915, 667)],
    "Space 36": [(915, 667), (1045, 667), (1045, 721), (915, 721)],
    "Space 37": [(915, 721), (1045, 721), (1045, 775), (915, 775)],
    "Space 38": [(915, 775), (1045, 775), (1045, 829), (915, 829)],
    "Space 39": [(460, 385), (515, 385), (515, 535), (460, 535)],
    "Space 40": [(515, 385), (570, 385), (570, 535), (515, 535)],
    "Space 41": [(570, 385), (625, 385), (625, 535), (570, 535)],
    "Space 42": [(625, 385), (680, 385), (680, 535), (625, 535)],
    "Space 43": [(680, 385), (735, 385), (735, 535), (680, 535)],
    "Space 44": [(460, 535), (515, 535), (515, 685), (460, 685)],
    "Space 45": [(515, 535), (570, 535), (570, 685), (515, 685)],
    "Space 46": [(570, 535), (625, 535), (625, 685), (570, 685)],
    "Space 47": [(625, 535), (680, 535), (680, 685), (625, 685)],
    "Space 48": [(680, 535), (735, 535), (735, 685), (680, 685)],
}

sx = 3.0726
sy = 2.9428
tx = -20.8
ty = -75.4

scaled_map = {}
for name, box in PARKING_MAP.items():
    new_box = []
    for x, y in box:
        nx = int(x * sx + tx)
        ny = int(y * sy + ty)
        new_box.append((nx, ny))
    scaled_map[name] = new_box

# Create distance transform to find nearest white pixels
dist_transform = cv2.distanceTransform(255 - thresh, cv2.DIST_L2, 3)

# Function to snap a line segment to the nearest white ridge
def snap_line(p1, p2):
    # This is complex, let's just do a simple search for the whole box translation
    return p1, p2

# Let's just output the scaled map to see how good it is.
with open('scaled_map.json', 'w') as f:
    json.dump(scaled_map, f, indent=4)

# Draw on image
annotated = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
for name, box in scaled_map.items():
    pts = np.array(box, np.int32).reshape((-1, 1, 2))
    cv2.polylines(annotated, [pts], True, (0, 0, 255), 3)

# Downscale for saving so it's not huge
small = cv2.resize(annotated, (0,0), fx=0.25, fy=0.25)
cv2.imwrite('debug_scaled.png', small)
