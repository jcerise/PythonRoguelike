from MapComponents import Tile


class AbstractMap:
    def __init__(self, map_width, map_height):
        self.map = []
        self.map_width = map_width
        self.map_height = map_height

    def make_map(self):
        self.map = [
            [Tile(False)
                for y in range(self.map_height)]
                    for x in range(self.map_width)]
        return self.map