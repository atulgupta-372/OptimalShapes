from shapely.geometry import Polygon
from shapely.affinity import rotate, translate

class TrianglePacker:
    def __init__(self, sheet_width, sheet_height, triangles):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.triangles = sorted(triangles, key=lambda t: -self.triangle_area(t))  # Sort largest first
        self.placed_triangles = []
        self.grid = [['.' for _ in range(self.sheet_width)] for _ in range(self.sheet_height)]  # ASCII grid

    def triangle_area(self, triangle):
        """Calculate the area of a triangle given its three points."""
        return abs((triangle[0][0] * (triangle[1][1] - triangle[2][1]) +
                    triangle[1][0] * (triangle[2][1] - triangle[0][1]) +
                    triangle[2][0] * (triangle[0][1] - triangle[1][1])) / 2)

    def is_valid_placement(self, triangle):
        """Check if a triangle fits within the sheet and does not overlap with existing ones."""
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
        """Place triangles efficiently using rotation and placement optimization."""
        for triangle_index, triangle in enumerate(self.triangles):
            for angle in [0, 90, 180, 270]:  # Try different rotations
                rotated_triangle = [rotate(Polygon(triangle), angle, origin=(0, 0)).exterior.coords[:-1]]

                for x in range(0, self.sheet_width, 1):  # Small step size for precise fit
                    for y in range(0, self.sheet_height, 1):
                        translated_triangle = [(px + x, py + y) for px, py in rotated_triangle[0]]
                        if self.is_valid_placement(translated_triangle):
                            self.placed_triangles.append(Polygon(translated_triangle))
                            self.mark_triangle_on_grid(translated_triangle, triangle_index)
                            break  # Stop once we find a valid placement
                    else:
                        continue
                    break

                if len(self.placed_triangles) == triangle_index + 1:
                    break  # Move to next triangle after placement

    def mark_triangle_on_grid(self, triangle, triangle_index):
        """Mark the triangle's position on the grid using ASCII characters."""
        char = chr(65 + (triangle_index % 26))  # Use 'A' to 'Z' for different triangles
        for px, py in triangle:
            if 0 <= int(px) < self.sheet_width and 0 <= int(py) < self.sheet_height:
                self.grid[int(py)][int(px)] = char  # Flip y-axis for correct ASCII display

    def display_grid(self):
        """Print the rectangle sheet with placed triangles."""
        print("\n".join("".join(row) for row in reversed(self.grid)))  # Reverse to match coordinate system

# Define sheet size and triangles
sheet_width = 20
sheet_height = 10
triangles = [
    [(0, 0), (5, 0), (2, 3)],  # Small triangle
    [(0, 0), (6, 0), (3, 4)],  # Medium triangle
    [(0, 0), (8, 0), (4, 5)],  # Large triangle
    [(0, 0), (4, 0), (2, 3)],
    [(0, 0), (7, 0), (3, 4)]
]

# Run the optimized triangle packing
packer = TrianglePacker(sheet_width, sheet_height, triangles)
packer.place_triangles()
packer.display_grid()
