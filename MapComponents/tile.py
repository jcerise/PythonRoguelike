class Tile:
    # Represents a single tile on a map, and its properties
    def __init__(self, block_move, block_sight=None):
        self.block_move = block_move

        # By default, if a tile blocks movement, it also blocks sight
        if block_sight is None:
            block_sight = block_move
        self.block_sight = block_sight