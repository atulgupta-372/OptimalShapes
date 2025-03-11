from shapely.geometry import Polygon
from shapely.affinity import translate
import random

class TrianglePacker:
    def __init__(self, sheet_width, sheet_height, triangles):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.triangles = sorted(triangles, key=lambda t: -self.triangle_area(t))  # Sort by area (largest first)
        self.placed_triangles = []
    
    def triangle_area(self, triangle):
        """Calculate the area of a triangle given its three points."""
        return abs((triangle[0][0] * (triangle[1][1] - triangle[2][1]) +
                    triangle[1][0] * (triangle[2][1] - triangle[0][1]) +
                    triangle[2][0] * (triangle[0][1] - triangle[1][1])) / 2)

    def is_valid_placement(self, triangle):
        """Check if a triangle fits within the sheet and doesn't overlap with existing ones."""
        triangle_polygon = Polygon(triangle)

        # Check if it fits inside the sheet
        if not (0 <= min(x for x, y in triangle) and max(x for x, y in triangle) <= self.sheet_width and
                0 <= min(y for x, y in triangle) and max(y for x, y in triangle) <= self.sheet_height):
            return False

        # Check for overlap with existing triangles
        for placed in self.placed_triangles:
            if triangle_polygon.intersects(placed):
                return False

        return True

    def place_triangles(self):
        """Greedily place triangles in the sheet."""
        for triangle in self.triangles:
            for x in range(0, self.sheet_width, 5):  # Small step to check placement
                for y in range(0, self.sheet_height, 5):
                    translated_triangle = [(px + x, py + y) for px, py in triangle]
                    if self.is_valid_placement(translated_triangle):
                        self.placed_triangles.append(Polygon(translated_triangle))
                        break  # Move to next triangle after placing
                else:
                    continue
                break

    def show_results(self):
        """Print the placement results."""
        print(f"Total Triangles Placed: {len(self.placed_triangles)}")
        print(f"Waste Space Estimate: {self.calculate_waste()}")

    def calculate_waste(self):
        """Estimate waste space by comparing total used area vs. sheet area."""
        used_area = sum(tri.area for tri in self.placed_triangles)
        return (1 - (used_area / (self.sheet_width * self.sheet_height))) * 100

# Example: Rectangle sheet size and triangles with their coordinates
sheet_width = 100
sheet_height = 100
triangles = [
    [(0, 0), (10, 0), (5, 8)],  # Example triangles
    [(0, 0), (20, 0), (10, 15)],
    [(0, 0), (15, 0), (7, 12)],
]

packer = TrianglePacker(sheet_width, sheet_height, triangles)
packer.place_triangles()
packer.show_results()
