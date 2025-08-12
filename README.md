<img width="960" height="960" alt="image" src="https://github.com/user-attachments/assets/f6ce7a88-67bc-41ac-99a5-ab254f54bccf" />
import cv2

# Load the PNG image
img = cv2.imread("apple.png")
if img is None:
    print("Error: Could not load apple.png")
    exit()

# Convert to grayscale and blur to reduce noise
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Check if contours were found
if not contours:
    print("Error: No apple detected")
    exit()

# Get the largest contour (assumed to be the apple)
largest_contour = max(contours, key=cv2.contourArea)

# Get bounding box for the apple
x, y, w, h = cv2.boundingRect(largest_contour)
apple_length_pixels = max(w, h)  # Length is the longer dimension

print(f"Apple length: {apple_length_pixels} pixels")

# Draw bounding box and save output for verification
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imwrite("output.png", img)
print("Output saved as output.png")
