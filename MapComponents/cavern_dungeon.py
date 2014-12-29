from random import randrange


class CavernDungeon:
    # A cavern dungeon layout (uneven rooms, corridors and general layout). Built using a cellular automata algorithm
    def __init__(self, tile_map, map_width, map_height):
        self.tile_map = tile_map
        self.map = tile_map.map
        self.map_width = map_width
        self.map_height = map_height

    def carve_layout(self):
        # Generate a cavern type map using Cellular Automata (similar to game of life). The map is usually free of
        # disjoint segments (disconnected areas), but not always, and does a good job of making sure there are no
        # large, open area

        # Next, make roughly 40% of the map wall tiles
        for x in range(0, len(self.map)):
            for y in range(0, len(self.map[x])):
                if randrange(0, 100) < 42:
                    self.map[x][y].block_move = True
                    self.map[x][y].block_sight = True

        # Now, we make several passes over the map, altering the wall tiles on each pass
        # If a tile has 5 or more neighbors (one tile away) that are walls, then that tile becomes a wall. If it has two
        # or fewer walls near (two or fewer tiles away) it, it also becomes a wall
        # (This gets rid of large empty spaces). If neither of these are true, the tile becomes a floor. This is
        # repeated several times to smooth out the "noise"
        for _ in range(5):
            for x in range(0, len(self.map)):
                for y in range(0, len(self.map[x])):
                    wall_count_one_away = self.count_walls_n_steps_away(self.map, 1, x, y)
                    wall_count_two_away = self.count_walls_n_steps_away(self.map, 2, x, y)
                    tile = self.map[x][y]
                    if wall_count_one_away >= 5 or wall_count_two_away <= 2:
                        # This tile becomes a wall
                        tile.block_move = True
                        tile.block_sight = True
                    else:
                        tile.block_move = False
                        tile.block_sight = False

        # Finally, we make a few more passes to smooth out caverns a little more, and get rid of isolated, single tile
        # walls
        for _ in range(4):
            for x in range(0, len(self.map)):
                for y in range(0, len(self.map[x])):
                    wall_count_one_away = self.count_walls_n_steps_away(self.map, 1, x, y)
                    tile = self.map[x][y]
                    if wall_count_one_away >= 5:
                        # This tile becomes a wall
                        tile.block_move = True
                        tile.block_sight = True
                    else:
                        tile.block_move = False
                        tile.block_sight = False

        # Now that we have the cavern generated, we need to remove any small, unattached caverns, as these will make it
        # more difficult to generate a starting position for the player

        # First, create a variable to store all the different sub-caverns in our larger cavern system. These are floor
        # areas not connected to any other cavern (separated by wall segments)
        caverns = []

        # Before we do anything else, we need to seal up the edges of the map, so the player cannot wander out into
        # nothingness. We do this by walking around the edges of the map and making them all wall
        for x in range(self.map_width):
            for y in range(self.map_height):
                if x == 0 or y == 0 or x == self.map_width - 1 or y == self.map_height - 1:
                    self.map[x][y].block_sight = True
                    self.map[x][y].block_move = True

        # Now, begin looping through the map, looking for individual caverns
        for x in range(self.map_width):
            for y in range(self.map_height):
                # Grab the tile at the current coordinates
                tile = self.map[x][y]

                # Set up some empty arrays to hold our current cavern
                cavern = []
                total_cavern_area = []

                # Ensure this is a non-wall tile that has not already been visited
                if not tile.visited and not tile.is_wall():
                    # If it meets the criteria, add it to the new cavern
                    cavern.append(tile)

                    # Loop through all potentially valid cavern tiles for this cavern, and see if they are actually part
                    # of the cavern or not. If they are, add them to the total, and grab all four of their neighbors
                    while len(cavern) > 0:
                        # Get the last item in the candidate list
                        node = cavern.pop()
                        if not node.visited and not node.is_wall():
                            # Mark the tile as visited
                            node.visit(True)
                            total_cavern_area.append(node)

                            # Append the tile to the west to the cavern array
                            if node.x - 1 > 0 and not self.map[node.x - 1][node.y].is_wall():
                                cavern.append(self.map[node.x - 1][node.y])
                            # the tile to the east to the cavern array
                            if node.x + 1 < len(self.map) and not self.map[node.x + 1][node.y].is_wall():
                                cavern.append(self.map[node.x + 1][node.y])
                            # Append the tile to the north to the cavern array
                            if node.y - 1 > 0 and not self.map[node.x][node.y - 1].is_wall():
                                cavern.append(self.map[node.x][node.y - 1])
                            # Append the tile to the south to the cavern array
                            if node.y + 1 < len(self.map[x]) and not self.map[node.x][node.y + 1].is_wall():
                                cavern.append(self.map[node.x][node.y + 1])

                    # Cavern detection and construction completed, so append this cavern to the list of all caverns
                    caverns.append(total_cavern_area)
                else:
                    # This was not a valid cavern candidate, so mark it as visited so we dont bother with it again
                    tile.visit(True)

        # Sort the cavern arrays so the largest cavern (the main cavern) is the last item, then remove it from the list
        # All the remaining caverns will be filled in
        sorted_caverns = sorted(caverns, lambda x,y: 1 if len(x)>len(y) else -1 if len(x)<len(y) else 0)
        main_cave = sorted_caverns.pop()

        # Fill in each of the remaining caverns, as they are not part of the main cave. This will ensure that every
        # part of the cavern system is accessible to the player
        for cave in sorted_caverns:
            for tile in cave:
                tile.block_move = True
                tile.block_sight = True

        # Finally, randomly place the player somewhere in the main cavern. we know it will be on a free, non-wall tile
        # since the cavern array only contains non-wall tiles
        random_tile = main_cave[randrange(0, len(main_cave))]
        (player_start_x, player_start_y) = (random_tile.x, random_tile.y)

        return player_start_x, player_start_y

    def count_walls_n_steps_away(self, map, n, x, y):
        # Count the number of wall tiles that are within n tiles of the source tile at (x, y)
        wall_count = 0

        for r in (-n, 0, n):
            for c in (-n, 0, n):
                try:
                    if map[x + r][y + c].is_wall():
                        wall_count += 1
                except IndexError:
                    # Check to see if the coordinates are off the map. Off map is considered wall
                    wall_count += 1

        return wall_count