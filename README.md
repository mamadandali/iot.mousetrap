<img width="960" height="960" alt="image" src="https://github.com/user-attachments/assets/f6ce7a88-67bc-41ac-99a5-ab254f54bccf" />
import cv2

# Load the image
img = cv2.imread("apple.png")
if img is None:
    print("Error: Could not load apple.png. Check if the file exists and path is correct.")
    exit()

# Display the image in a window
cv2.imshow("OpenCV Test", img)

# Wait for a key press and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

print("OpenCV is working! Image displayed successfully.")
