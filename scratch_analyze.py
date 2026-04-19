import cv2
import numpy as np
import json

img = cv2.imread('IMG_0764.png', 0)

# The image is 3508x2480
# Let's find all the white pixels
y_coords, x_coords = np.where(img > 128)

# Print some stats about the white pixels
print("Total white pixels:", len(y_coords))
print("X range:", x_coords.min(), x_coords.max())
print("Y range:", y_coords.min(), y_coords.max())

# Let's see if we can find the scaling factor by comparing the agent's bounding box sizes
# to the image dimensions.
# The agent found X range roughly 205 to 1045.
# The image X range is probably around 0 to 3508.
# 1045 - 205 = 840. The actual image might have parking spots covering ~ 840 * scale.
