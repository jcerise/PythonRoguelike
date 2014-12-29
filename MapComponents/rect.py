class Rect:
    # Represents a rectangle on the map. Used to characterize a room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        # Return the center coordinates of this rectangle
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return center_x, center_y

    def intersect(self, other):
        # Return True if this rectangle intersects another one
        return (self.x1 <= other.x2 and self.x2 >= other.x2 and
                self.y1 <= other.y1 and self.y2 >= other.y2)