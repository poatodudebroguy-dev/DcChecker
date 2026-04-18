import cv2
import numpy as np

# Global variables to track state
current_points = []
all_polygons = {}
img_display = None

def mouse_handler(event, x, y, flags, param):
    global current_points, img_display
    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append((x, y))
        print(f"Point added: ({x}, {y})")
        
        # Draw a point and a line to the previous point
        cv2.circle(img_display, (x, y), 4, (0, 255, 0), -1)
        if len(current_points) > 1:
            cv2.line(img_display, current_points[-2], current_points[-1], (0, 255, 0), 2)
        
        cv2.imshow("Coordinate Picker", img_display)

        if len(current_points) == 4:
            # Close the polygon visually
            cv2.line(img_display, current_points[3], current_points[0], (0, 255, 0), 2)
            cv2.imshow("Coordinate Picker", img_display)
            
            spot_name = input("Enter name for this parking spot (e.g., Space A1): ")
            all_polygons[spot_name] = current_points.copy()
            print(f"Added {spot_name}: {current_points}")
            print("--- Click 4 points for the next spot, or press 'q' to finish and get code ---")
            current_points = []

def start_picker(image_path):
    global img_display
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image at {image_path}. Check the filename!")
        return

    img_display = img.copy()
    cv2.namedWindow("Coordinate Picker")
    cv2.setMouseCallback("Coordinate Picker", mouse_handler)

    print("INSTRUCTIONS:")
    print("1. Click the 4 corners of a parking spot in order (clockwise or counter-clockwise).")
    print("2. Look at your terminal/command prompt to enter the spot name after the 4th click.")
    print("3. Repeat for all spots.")
    print("4. Press 'q' on the image window when finished.")

    while True:
        cv2.imshow("Coordinate Picker", img_display)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("\n--- COPY AND PASTE THIS INTO YOUR bot.py ---")
    print(f"PARKING_MAP = {all_polygons}")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Using .png as per your file format. 
    # Replace 'parking_lot.png' with your actual filename.
    start_picker("parking_lot.png")
