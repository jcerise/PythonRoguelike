from MapComponents import AbstractMap
import libtcodpy as libtcod
from Actor import Actor

# Window width and height
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Map width and height (slightly smaller for now to allow for message area)
MAP_WIDTH = 80
MAP_HEIGHT = 45

# Colors for wall and floor tiles
color_dark_wall = libtcod.Color(63, 63, 63)
color_light_wall = libtcod.Color(159, 159, 159)
color_dark_ground = libtcod.Color(63, 50, 31)
color_light_ground = libtcod.Color(158, 134, 100)


def handle_keys():

    key = libtcod.console_wait_for_keypress(True)
    if key == libtcod.KEY_ENTER and libtcod.KEY_ALT:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    global player
    # Move the player. Before each movement, get the tile the player wants to move to, so it can be checked for validity
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        tile = tile_map.map[player.x][player.y - 1]
        player.move(0, -1, tile)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        tile = tile_map.map[player.x][player.y + 1]
        player.move(0, 1, tile)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        tile = tile_map.map[player.x + 1][player.y]
        player.move(1, 0, tile)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        tile = tile_map.map[player.x - 1][player.y]
        player.move(-1, 0, tile)


def render_all():
    # Draw map tiles to the console
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = tile_map.map[x][y].block_sight
            if wall:
                libtcod.console_put_char_ex(con, x, y, '#', color_light_wall, libtcod.black)
            else:
                libtcod.console_put_char_ex(con, x, y, '.', color_light_ground, libtcod.black)

    # Draw actors to the console
    for actor in actors:
        actor.draw()

    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

#############################################
# Initialization and Main Loop
#############################################

libtcod.console_set_custom_font('font/arial.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Generic Python Roguelike', False)

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Actor(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, '@', libtcod.white, con)
npc = Actor(4, 4, 'L', libtcod.yellow, con)

# Generate the map for the particular level
tile_map = AbstractMap(MAP_WIDTH, MAP_HEIGHT)
tile_map.make_map()

tile_map.map[30][22].block_move = True
tile_map.map[30][22].block_sight = True
tile_map.map[50][22].block_move = True
tile_map.map[50][22].block_sight = True

while not libtcod.console_is_window_closed():

    actors = [npc, player]
    render_all()
    libtcod.console_flush()

    for actor in actors:
        actor.clear()

    # Handle keys and exit the game if needed
    exit_game = handle_keys()
    if exit_game:
        break