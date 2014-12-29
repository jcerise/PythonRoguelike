from MapComponents import Tile


class AbstractMap:
    def __init__(self, map_width, map_height):
        self.map = []
        self.map_width = map_width
        self.map_height = map_height

    def make_map(self):
        self.map = [
            [Tile(True)
                for y in range(self.map_height)]
                    for x in range(self.map_width)]

        return self.map

    def create_room(self, rect):
        # Iterate through the tiles encompassed by th rectangle, and make them passable
        for x in range(rect.x1 + 1, rect.x2):
            for y in range(rect.y1 + 1, rect.y2):
                self.map[x][y].block_move = False
                self.map[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y].block_move = False
            self.map[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x][y].block_move = False
            self.map[x][y].block_sight = False