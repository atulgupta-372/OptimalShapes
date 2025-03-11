import cv2
import numpy as np

# Load the image
image = cv2.imread('shapes3.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding or Canny edge detection to highlight the shapes
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the thresholded image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over each contour and draw it on the image
for contour in contours:
    # Draw the contour on the image (using green color and thickness 2)
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)  # Green contours with thickness of 2

# Display the image with contours
cv2.imshow('Image with Contours', image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
