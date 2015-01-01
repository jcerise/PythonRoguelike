from MapComponents import AbstractMap, StandardDungeon, CavernDungeon
import libtcodpy as libtcod
from Actor import Actor

# Window width and height
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Size of the map portion actually shown on the screen
CAMERA_WIDTH = 80
CAMERA_HEIGHT = 43
camera_x, camera_y = 0, 0

# Map width and height (slightly smaller for now to allow for message area)
MAP_WIDTH = 200
MAP_HEIGHT = 200

# Define FOV constants
FOV_ALGORITHM = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 6
fov_recompute = True

# Colors for wall and floor tiles
color_dark_wall = libtcod.Color(63, 63, 63)
color_light_wall = libtcod.Color(159, 159, 159)
color_dark_ground = libtcod.Color(63, 50, 31)
color_light_ground = libtcod.Color(158, 134, 100)


def move_camera(target_x, target_y):
    global camera_x, camera_y, fov_recompute
    # new camera coordinates (top-left corner of the screen relative to the map)
    x = target_x - CAMERA_WIDTH / 2  #coordinates so that the target is at the center of the screen
    y = target_y - CAMERA_HEIGHT / 2

    # make sure the camera doesn't see outside the map
    if x < 0: x = 0
    if y < 0: y = 0
    if x > MAP_WIDTH - CAMERA_WIDTH - 1: x = MAP_WIDTH - CAMERA_WIDTH - 1
    if y > MAP_HEIGHT - CAMERA_HEIGHT - 1: y = MAP_HEIGHT - CAMERA_HEIGHT - 1

    if x != camera_x or y != camera_y: fov_recompute = True

    (camera_x, camera_y) = (x, y)


def to_camera_coordinates(x, y):
    # Convert coordinates on the map to coordinates on the screen
    x, y = (x - camera_x, y - camera_y)

    if x < 0 or y < 0 or x >= CAMERA_WIDTH or y >= CAMERA_HEIGHT:
        return None, None  # If its outside the view, return nothing
    return x, y


def handle_keys():

    key = libtcod.console_wait_for_keypress(True)
    if key == libtcod.KEY_ENTER and libtcod.KEY_ALT:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    global player, fov_recompute
    # Move the player. Before each movement, get the tile the player wants to move to, so it can be checked for validity
    # Also, set the FOV to recompute after each move, so the FOV map is up to date
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        tile = tile_map.map[player.x][player.y - 1]
        player.move(0, -1, tile)
        fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        tile = tile_map.map[player.x][player.y + 1]
        player.move(0, 1, tile)
        fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        tile = tile_map.map[player.x + 1][player.y]
        player.move(1, 0, tile)
        fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        tile = tile_map.map[player.x - 1][player.y]
        player.move(-1, 0, tile)
        fov_recompute = True


def render_all():
    # Check if the FOV map needs to be recomputed
    global fov_recompute

    move_camera(player.x, player.y)

    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)
        libtcod.console_clear(con)

        # Draw map tiles to the console
        for y in range(CAMERA_HEIGHT):
            for x in range(CAMERA_WIDTH):
                map_x, map_y = camera_x + x, camera_y + y
                # Check to see if the current tile is visible
                visible = libtcod.map_is_in_fov(fov_map, map_x, map_y)
                wall = tile_map.map[map_x][map_y].block_sight
                if not visible:
                    # Check if the player has explored this yet or not. If not, do not show it. If so, display it darkened.
                    if tile_map.map[map_x][map_y].explored:
                        if wall:
                            libtcod.console_put_char_ex(con, x, y, '#', color_dark_wall, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(con, x, y, '.', color_dark_ground, libtcod.black)
                else:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, '#', color_light_wall, libtcod.black)
                    else:
                        libtcod.console_put_char_ex(con, x, y, '.', color_light_ground, libtcod.black)
                    tile_map.map[map_x][map_y].explored = True

    # Draw actors to the console
    for actor in actors:
        if libtcod.map_is_in_fov(fov_map, actor.x, actor.y):
            x, y = to_camera_coordinates(actor.x, actor.y)

            if x is not None:
                actor.draw(x, y)

    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)

#############################################
# Initialization and Main Loop
#############################################

libtcod.console_set_custom_font('font/arial.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Generic Python Roguelike', False)

con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)

player = Actor(25, 23, '@', libtcod.white, con)

# Generate the map for the particular level
tile_map = AbstractMap(MAP_WIDTH, MAP_HEIGHT)
tile_map.make_map()

if libtcod.random_get_int(0, 0, 1) == 1:
    dungeon = StandardDungeon(tile_map, 10, 6, 50, MAP_WIDTH, MAP_HEIGHT)
else:
    dungeon = CavernDungeon(tile_map, MAP_WIDTH, MAP_HEIGHT)

# Carve the dungeon layout, and set the players starting coordinates
player.x, player.y = dungeon.carve_layout()

# Generate an FOV map
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not tile_map.map[x][y].block_sight, not tile_map.map[x][y].block_move)

while not libtcod.console_is_window_closed():

    actors = [player]
    render_all()
    libtcod.console_flush()

    for actor in actors:
        actor.clear()

    # Handle keys and exit the game if needed
    exit_game = handle_keys()
    if exit_game:
        break