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

def can_place(sheet, x, y, width, height):
    sheet_height, sheet_width, _ = sheet.shape
    return x + width <= sheet_width and y + height <= sheet_height

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
    positions = []

    x, y = 0, 0
    max_row_height = 0

    for shape in sorted(shapes, key=lambda s: s.get_bounding_box()[0] * s.get_bounding_box()[1], reverse=True):
        width, height = shape.get_bounding_box()

        if can_place(sheet, x, y, width, height):
            shape.placed = True
            shape.position = (x, y)
            positions.append((x, y, width, height))
            draw_shape(sheet, shape, x, y)
            x += width
            max_row_height = max(max_row_height, height)
        else:
            x = 0
            y += max_row_height
            max_row_height = 0
            if can_place(sheet, x, y, width, height):
                shape.placed = True
                shape.position = (x, y)
                positions.append((x, y, width, height))
                draw_shape(sheet, shape, x, y)
                x += width
                max_row_height = max(max_row_height, height)

    return sheet

# Example Usage
shapes = [
    Shape("rectangle", (100, 50)),
    Shape("circle", (30,)),
    Shape("square", (40,)),
    Shape("triangle", (60, 30)),
    Shape("rectangle", (80, 40))
]

sheet_size = (300, 500)  # Sheet size (height, width)
sheet = pack_shapes(sheet_size, shapes)

cv2.imshow("Packed Sheet", sheet)
cv2.waitKey(0)
cv2.destroyAllWindows()