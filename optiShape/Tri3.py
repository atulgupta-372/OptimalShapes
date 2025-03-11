import cv2
import numpy as np

class Parallelogram:
    def __init__(self, base, height, angle=0):
        # Parallelogram's base, height, and angle (in degrees)
        self.base = base
        self.height = height
        self.angle = angle  # Rotation angle (degrees)
        self.position = (0, 0)

    def get_bounding_box(self):
        # Calculate the bounding box for the parallelogram (ignores rotation)
        return (self.base, self.height)

    def rotate(self, angle):
        # Update the angle of rotation
        self.angle += angle

    def get_rotated_points(self, x, y):
        # Get the 4 points of the parallelogram after rotation
        angle_rad = np.radians(self.angle)
        # Points before rotation
        points = np.array([
            [x, y],  # Bottom-left
            [x + self.base, y],  # Bottom-right
            [x + self.base - self.height * np.tan(angle_rad), y + self.height],  # Top-right
            [x - self.height * np.tan(angle_rad), y + self.height]  # Top-left
        ], dtype=np.float32)

        # Rotation matrix
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad), np.cos(angle_rad)]
        ])
        # Rotate points around the bottom-left corner (x, y)
        rotated_points = np.dot(points - [x, y], rotation_matrix) + [x, y]
        return rotated_points.astype(np.int32)

def can_place(sheet, parallelogram, x, y, occupied):
    # Check if the parallelogram can be placed at (x, y) without overlapping
    rotated_points = parallelogram.get_rotated_points(x, y)
    
    # Check if any part of the parallelogram goes out of bounds
    if np.any(rotated_points[:, 0] < 0) or np.any(rotated_points[:, 0] >= sheet.shape[1]) or \
       np.any(rotated_points[:, 1] < 0) or np.any(rotated_points[:, 1] >= sheet.shape[0]):
        return False

    # Check for overlap with other parallelograms
    for ox, oy, ow, oh in occupied:
        if not (x + ow <= ox or x >= ox + ow or y + oh <= oy or y >= oy + oh):
            return False
    return True

def draw_parallelogram(sheet, parallelogram, x, y):
    # Draw the parallelogram on the sheet
    rotated_points = parallelogram.get_rotated_points(x, y)
    color = tuple(np.random.randint(0, 255, 3).tolist())
    cv2.fillPoly(sheet, [rotated_points], color)

def place_parallelograms(sheet_size, parallelograms):
    sheet = np.ones((sheet_size[0], sheet_size[1], 3), dtype=np.uint8) * 255
    occupied = []

    for parallelogram in parallelograms:
        placed = False
        for y in range(sheet_size[0]):
            for x in range(sheet_size[1]):
                # Try to place the parallelogram at every possible position and check if it fits
                if can_place(sheet, parallelogram, x, y, occupied):
                    parallelogram.position = (x, y)
                    occupied.append((x, y, parallelogram.base, parallelogram.height))
                    draw_parallelogram(sheet, parallelogram, x, y)
                    placed = True
                    break
            if placed:
                break
    return sheet

# Example usage:
parallelograms = [
    Parallelogram(60, 30, angle=0),
    Parallelogram(80, 40, angle=30),
    Parallelogram(100, 50, angle=45),
    Parallelogram(40, 20, angle=60),
    Parallelogram(50, 30, angle=90)
]

sheet_size = (500, 500)  # Rectangular sheet size
sheet = place_parallelograms(sheet_size, parallelograms)

# Display the result
cv2.imshow("Packed Parallelograms", sheet)
cv2.waitKey(0)
cv2.destroyAllWindows()
