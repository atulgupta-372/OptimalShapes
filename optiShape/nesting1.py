import tkinter as tk
import math

# Function to rotate a point (x, y) around the origin (0, 0) by angle theta (in radians)
def rotate_point(x, y, angle):
    return (x * math.cos(angle) - y * math.sin(angle),
            x * math.sin(angle) + y * math.cos(angle))

class Part:
    def __init__(self, points):
        self.original_points = points  # List of (x, y) coordinates for the shape
        self.points = points  # Current points after rotation
        self.rotated = False

    def rotate(self):
        # Rotate all points by 90 degrees (π/2 radians)
        self.points = [rotate_point(x, y, math.pi / 2) for x, y in self.original_points]
        self.rotated = not self.rotated


class Sheet:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.used_area = 0
        self.parts = []

    def fits(self, part, x_offset, y_offset):
        # Check if the part fits in the given position (no overlap)
        min_x = min(part.points, key=lambda p: p[0])[0]
        max_x = max(part.points, key=lambda p: p[0])[0]
        min_y = min(part.points, key=lambda p: p[1])[1]
        max_y = max(part.points, key=lambda p: p[1])[1]

        # Check if the shape fits inside the sheet
        if min_x + x_offset < 0 or max_x + x_offset > self.width or min_y + y_offset < 0 or max_y + y_offset > self.height:
            return False

        # Check for overlap with already placed parts
        for placed_part in self.parts:
            placed_min_x = min(placed_part.points, key=lambda p: p[0])[0] + placed_part.x_offset
            placed_max_x = max(placed_part.points, key=lambda p: p[0])[0] + placed_part.x_offset
            placed_min_y = min(placed_part.points, key=lambda p: p[1])[1] + placed_part.y_offset
            placed_max_y = max(placed_part.points, key=lambda p: p[1])[1] + placed_part.y_offset

            if not (max_x + x_offset < placed_min_x or min_x + x_offset > placed_max_x or max_y + y_offset < placed_min_y or min_y + y_offset > placed_max_y):
                return False  # Overlap found

        return True

    def add_part(self, part, x_offset, y_offset):
        self.parts.append(part)
        part.x_offset = x_offset
        part.y_offset = y_offset
        min_x = min(part.points, key=lambda p: p[0])[0]
        max_x = max(part.points, key=lambda p: p[0])[0]
        min_y = min(part.points, key=lambda p: p[1])[1]
        max_y = max(part.points, key=lambda p: p[1])[1]
        self.used_area += (max_x - min_x) * (max_y - min_y)  # Simple bounding box area for now


class NestingApp:
    def __init__(self, root, sheet_width, sheet_height):
        self.root = root
        self.root.title("Arbitrary Shape Nesting")
        
        # Create the canvas for drawing the sheet and parts
        self.canvas = tk.Canvas(root, width=sheet_width, height=sheet_height)
        self.canvas.pack()
        
        # Define a Sheet and Part objects
        self.sheet = Sheet(sheet_width, sheet_height)
        
        # Sample parts (arbitrary shapes represented by lists of points)
        self.parts = [
            Part([(0, 0), (60, 0), (60, 70), (0, 70)]),  # Rectangle 60x70
            Part([(0, 0), (40, 0), (30, 40), (10, 40)]),  # Irregular shape
            Part([(0, 0), (40, 0), (40, 50), (0, 50)]),  # Rectangle 40x50
            Part([(0, 0), (30, 0), (30, 40), (0, 40)]),  # Rectangle 30x40
            Part([(0, 0), (10, 0), (10, 20), (0, 20)])   # Rectangle 10x20
        ]
        
        # Perform the nesting process
        self.nest_parts()
        self.draw_nesting()

    def nest_parts(self):
        # Sort parts by area (largest first)
        self.parts.sort(key=lambda part: self.calculate_area(part), reverse=True)

        # Attempt to place each part on the sheet
        x_offset = 10
        y_offset = 10
        for part in self.parts:
            # Try fitting part in its original orientation
            if self.sheet.fits(part, x_offset, y_offset):
                self.sheet.add_part(part, x_offset, y_offset)
            # Try rotating the part and fit
            elif self.sheet.fits(Part(part.points), x_offset, y_offset):
                part.rotate()
                self.sheet.add_part(part, x_offset, y_offset)
            else:
                # If it doesn't fit, move to the next row (simple heuristic)
                x_offset = 10
                y_offset += 50  # Adjust this based on part size to avoid overlap
                if self.sheet.fits(part, x_offset, y_offset):
                    self.sheet.add_part(part, x_offset, y_offset)

    def calculate_area(self, part):
        # Simple area calculation for a polygon (bounding box area for simplicity)
        min_x = min(part.points, key=lambda p: p[0])[0]
        max_x = max(part.points, key=lambda p: p[0])[0]
        min_y = min(part.points, key=lambda p: p[1])[1]
        max_y = max(part.points, key=lambda p: p[1])[1]
        return (max_x - min_x) * (max_y - min_y)

    def draw_nesting(self):
        # Draw the material sheet (rectangle)
        self.canvas.create_rectangle(10, 10, self.sheet.width - 10, self.sheet.height - 10, outline="black", width=2)

        # Draw parts on the canvas based on their position and size
        for part in self.sheet.parts:
            self.draw_part(part)
        
        # Display the total used area
        self.canvas.create_text(self.sheet.width / 2, self.sheet.height - 20, 
                                text=f"Used Area: {self.sheet.used_area} square units", fill="black", font=('Arial', 12))

    def draw_part(self, part):
        # Draw a polygon part by translating its points
        translated_points = [(x + part.x_offset, y + part.y_offset) for x, y in part.points]
        self.canvas.create_polygon(translated_points, fill="lightblue", outline="blue")


# Set up the main Tkinter window
root = tk.Tk()

# Define the sheet size (e.g., 500x500 units)
sheet_width = 500
sheet_height = 500

# Create the NestingApp instance
app = NestingApp(root, sheet_width, sheet_height)

# Run the Tkinter main loop
root.mainloop()
