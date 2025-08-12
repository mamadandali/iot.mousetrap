<img width="960" height="960" alt="image" src="https://github.com/user-attachments/assets/f6ce7a88-67bc-41ac-99a5-ab254f54bccf" />
import cv2
import numpy as np

# === CONFIG ===
image_path = "apple.png"
min_area = 500
# ==============

# Load image
img = cv2.imread(image_path)
if img is None:
    print(f"Error: Could not load {image_path}")
    exit()

# Convert to HSV for better color filtering
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Apple color range (adjust if needed)
# This example is for red apples; change for green/yellow
lower_red1 = np.array([0, 80, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 80, 50])
upper_red2 = np.array([180, 255, 255])

# Create masks for red
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1 | mask2

# Remove small noise
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

# Find contours on mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if not contours:
    print("Error: No apple detected by color filter")
    exit()

# Filter by area
valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
if valid_contours:
    largest_contour = max(valid_contours, key=cv2.contourArea)
else:
    largest_contour = max(contours, key=cv2.contourArea)

# Get bounding box
x, y, w, h = cv2.boundingRect(largest_contour)
apple_width_pixels = w
apple_height_pixels = h

# Draw bounding box and text
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.putText(img, f"Width: {apple_width_pixels}px", (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
cv2.putText(img, f"Height: {apple_height_pixels}px", (x, y - 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# Show and save
cv2.imshow("Apple Measurement", img)
cv2.imwrite("output.png", img)

print(f"Apple width: {apple_width_pixels} pixels")
print(f"Apple height: {apple_height_pixels} pixels")
print("Output saved as output.png")

cv2.waitKey(0)
cv2.destroyAllWindows()

