import libtcodpy as libtcod


class Actor:
    def __init__(self, x, y, char, color, con):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.con = con

    def move(self, dx, dy, tile):
        # Move by a given amount
        if not tile.block_move:
            self.x += dx
            self.y += dy

    def draw(self):
        # Set the character color, and then draw the actor to the console
        libtcod.console_set_default_foreground(self.con, self.color)
        libtcod.console_put_char(self.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # Erase the character that represents this actor
        libtcod.console_put_char(self.con, self.x, self.y, ' ', libtcod.BKGND_NONE)