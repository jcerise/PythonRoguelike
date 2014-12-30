class Tile:
    # Represents a single tile on a map, and its properties
    def __init__(self, x, y, block_move, block_sight=None):
        self.x = x
        self.y = y

        self.block_move = block_move

        # By default, if a tile blocks movement, it also blocks sight
        if block_sight is None:
            block_sight = block_move
        self.block_sight = block_sight

        self.visited = False
        self.explored = False

    def is_wall(self):
        # Check if this tile is a wall (blocks sight and movement)
        if self.block_move and self.block_sight:
            return True

    def is_chasm(self):
        # Check if this tile is a chasm (blocks movement, but not sight
        if self.block_move and not self.block_sight:
            return True

    def visit(self, visited):
        # Mark this tile as visited or not
        self.visited = visited