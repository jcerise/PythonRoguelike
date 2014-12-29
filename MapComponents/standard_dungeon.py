from MapComponents import Rect, Tile
import libtcodpy as libtcod


class StandardDungeon:
    # A standard dungeon, rooms of random size are placed within the map, and then connected

    def __init__(self, tile_map, room_max_size, room_min_size, max_rooms, map_width, map_height):
        self.tile_map = tile_map
        self.room_max_size = room_max_size
        self.room_min_size = room_min_size
        self.max_rooms = max_rooms
        self.map_width = map_width
        self.map_height = map_height

    def carve_layout(self):
        # First, make the entire map walls (it gets passed in as all floor)
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.tile_map.map[x][y].block_move = True
                self.tile_map.map[x][y].block_sight = True

        rooms = []
        num_rooms = 0

        for r in range(self.max_rooms):
            # Create a room with a random width and height, bounded by room_max_size and room_min_size
            w = libtcod.random_get_int(0, self.room_min_size, self.room_max_size)
            h = libtcod.random_get_int(0, self.room_min_size, self.room_max_size)
            # Create a random position within the map bounds for the room
            x = libtcod.random_get_int(0, 0, self.map_width - w - 1)
            y = libtcod.random_get_int(0, 0, self.map_height - h - 1)

            new_room = Rect(x, y, w, h)

            # Check for intersections with our new rooms and any previous rooms
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                # There were no intersections, so this is a valid room
                self.tile_map.create_room(new_room)
                cur_center_x, cur_center_y = new_room.center()

                if num_rooms > 0:
                    # This is not the first room, so connect it to a previous room via a tunnel
                    # Get the center coordinates of the previous room (rooms are connected at the center)
                    prev_center_x, prev_center_y = rooms[num_rooms - 1].center()

                    # Flip a coin to see how the tunnel will generate (horizontal then vertical, or vice versa)
                    if libtcod.random_get_int(0, 0, 1) == 1:
                        self.tile_map.create_h_tunnel(prev_center_x, cur_center_x, prev_center_y)
                        self.tile_map.create_v_tunnel(prev_center_y, cur_center_y, cur_center_x)
                    else:
                        self.tile_map.create_v_tunnel(prev_center_y, cur_center_y, prev_center_x)
                        self.tile_map.create_h_tunnel(prev_center_x, cur_center_x, cur_center_y)
                else:
                    # This is the first room, where the player starts, return the center coordinates
                    start_x, start_y = cur_center_x, cur_center_y

                rooms.append(new_room)
                num_rooms += 1

        return start_x, start_y
