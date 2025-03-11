import cv2
import numpy as np

class Shape:
    def __init__(self, shape_type, dims):
        self.type = shape_type
        self.dims = dims
        self.placed = False
        self.position = (0, 0)

    def get_bounding_box(self):
        if self.type == "circle":
            radius = self.dims[0]
            return (2 * radius, 2 * radius)
        elif self.type == "rectangle":
            return self.dims
        elif self.type == "square":
            return (self.dims[0], self.dims[0])
        elif self.type == "triangle":
            base, height = self.dims
            return (base, height)

def can_place(sheet, x, y, width, height, occupied):
    sheet_height, sheet_width, _ = sheet.shape
    if x + width > sheet_width or y + height > sheet_height:
        return False
    # Check if the position overlaps with already placed shapes
    for ox, oy, ow, oh in occupied:
        if not (x + width <= ox or x >= ox + ow or y + height <= oy or y >= oy + oh):
            return False
    return True

def draw_shape(sheet, shape, x, y):
    color = tuple(np.random.randint(0, 255, 3).tolist())
    if shape.type == "rectangle":
        w, h = shape.dims
        cv2.rectangle(sheet, (x, y), (x + w, y + h), color, -1)
    elif shape.type == "circle":
        r = shape.dims[0]
        cv2.circle(sheet, (x + r, y + r), r, color, -1)
    elif shape.type == "square":
        s = shape.dims[0]
        cv2.rectangle(sheet, (x, y), (x + s, y + s), color, -1)
    elif shape.type == "triangle":
        base, height = shape.dims
        pts = np.array([[x, y + height], [x + base, y + height], [x + base // 2, y]], np.int32)
        cv2.fillPoly(sheet, [pts], color)

def pack_shapes(sheet_size, shapes):
    sheet = np.ones((sheet_size[0], sheet_size[1], 3), dtype=np.uint8) * 255
    occupied = []  # List to store occupied areas (x, y, width, height)
    free_spaces = [(0, 0, sheet_size[1], sheet_size[0])]  # Initial full space (x, y, width, height)

    # Sort shapes: First place larger shapes first to prevent leaving gaps
    shapes_sorted = sorted(shapes, key=lambda s: s.get_bounding_box()[0] * s.get_bounding_box()[1], reverse=True)

    for shape in shapes_sorted:
        width, height = shape.get_bounding_box()

        # Try to place the shape in available free spaces
        placed = False
        for i, (fx, fy, fw, fh) in enumerate(free_spaces):
            if can_place(sheet, fx, fy, width, height, occupied):
                shape.placed = True
                shape.position = (fx, fy)
                occupied.append((fx, fy, width, height))  # Mark the area as occupied
                draw_shape(sheet, shape, fx, fy)
                
                # Update the free spaces by removing the used space and creating new free spaces
                if fx + width < fx + fw:
                    free_spaces.append((fx + width, fy, fw - width, height))
                if fy + height < fy + fh:
                    free_spaces.append((fx, fy + height, width, fh - height))
                
                # Remove the used free space
                free_spaces.pop(i)
                placed = True
                break

        if not placed:
            # If the shape couldn't be placed in the current free spaces, move to the next space
            continue

    return sheet

# Example Usage with Multiple Shapes including Very Small Ones

shapes = [
    Shape("rectangle", (100, 50)),
    Shape("circle", (50,)),
    Shape("circle", (30,)),
    Shape("circle", (20,)),
    Shape("square", (40,)),
    Shape("triangle", (60, 30)),
    Shape("rectangle", (80, 40)),
    Shape("rectangle", (200, 100)),
    Shape("circle", (10,)),  # Very small circle
    Shape("square", (10,)),  # Very small square
    Shape("triangle", (20, 10)),  # Small triangle
    Shape("triangle", (5, 15)),   # Very small triangle
    Shape("rectangle", (5, 5)),   # Very small rectangle
    Shape("circle", (5,))         # Very small circle
]

sheet_size = (300, 500)  # Sheet size (height, width)
sheet = pack_shapes(sheet_size, shapes)

cv2.imshow("Packed Sheet", sheet)
cv2.waitKey(0)
cv2.destroyAllWindows()
