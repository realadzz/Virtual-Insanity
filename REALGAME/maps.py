# all the maps
# this file holds all the map data, the grid layouts and what each tile means, plus a few plain functions for reading them I'm pretty sure this is what jacky meant by an argument

# every tile is drawn as a small block of characters instead of just one symbol, so the map looks less flat. Each block is TILE_HEIGHT lines tall and every line is TILE_WIDTH characters wide
TILE_WIDTH = 3
TILE_HEIGHT = 2

# each tile code (like "w" for wall) maps to what it means, whether it can trigger a battle, and the little "art" block used to draw it
MAPBIOM = {
    "w":  {"name": "wall",         "encounter": False, "art": ["███", "███"]},
    "e":  {"name": "entrance",     "encounter": False, "art": ["| |", "|_|"]},
    "f":  {"name": "floor",        "encounter": False, "art": ["   ", "   "]},
    "d":  {"name": "desk",         "encounter": False, "art": ["▄▄▄", "   "]},
    "s":  {"name": "start",        "encounter": False, "art": ["   ", "   "]},
    "g":  {"name": "glass shard",  "encounter": False, "art": [" ^ ", "   "]},
    "bh": {"name": "blue helmet",  "encounter": False, "art": [" ⌂ ", "   "]},
    "r":  {"name": "robot corpse", "encounter": True,  "art": ["x x", " x "]},
    "sp": {"name": "save point",   "encounter": False, "art": [" ✦ ", "   "]},
    "c":  {"name": "car wreck",    "encounter": False, "art": ["▄█▄", "o o"]},
    "j":  {"name": "junk pile",    "encounter": False, "art": ["░▒░", "▒░▒"]},
    "tw": {"name": "twinkly",      "encounter": False, "art": ["   ", " ★ "]},  # just the star, on the bottom row like the player
    # the ambush tile looks like normal floor on purpose, so the player doesn't see it coming
    "am": {"name": "floor",        "encounter": False, "art": ["   ", "   "]},
}

# tiles the player can't walk onto (bumping into them does nothing except show a message)
BLOCKING_TILES = ["w", "tw"]

# the character used to represent the player. If this shows up as a box or a question mark in the terminal, just keep the question mark or do like "P" or sum idk
PLAYER_SYMBOL = "𖨆"

PLAYER_ART = ["   ", " " + PLAYER_SYMBOL + " "]

# what an ally following the player looks like on the map (same look as twinkly's npc tile)
FOLLOWER_ART = MAPBIOM["tw"]["art"]

LAB_MAP = [
    ["w", "w", "w", "w", "w", "w"],
    ["w", "d", "d", "d", "sp", "e"],
    ["w", "f", "f", "f", "f", "e"],
    ["w", "s", "f", "f", "f", "w"],
    ["w", "f", "g", "f", "f", "w"],
    ["w", "f", "d", "d", "d", "w"],
    ["w", "w", "w", "w", "w", "w"],
]

RUINS_MAP = [
    ["w", "w", "w", "w", "w", "w"],
    ["w", "bh", "f", "r", "f", "e"],
    ["e", "f", "f", "f", "f", "e"],
    ["e", "f", "f", "f", "f", "w"],
    ["w", "f", "f", "f", "f", "w"],
    ["w", "r", "r", "r", "sp", "w"],
    ["w", "w", "w", "w", "w", "w"],
]

# the broken highway, where the ambush happens (the "am" column stretches top to bottom so the player can't sneak past it)
HIGHWAY_MAP = [
    ["w", "w", "w", "w", "w", "w", "w", "w"],
    ["e", "f", "f", "am", "f", "c", "f", "w"],
    ["e", "f", "f", "am", "f", "f", "f", "e"],
    ["w", "c", "f", "am", "c", "f", "j", "w"],
    ["w", "w", "w", "w", "w", "w", "w", "w"],
]

# twinkly's hideout inside the highway pillar
HIDEOUT_MAP = [
    ["w", "w", "w", "w", "w"],
    ["w", "sp", "f", "tw", "w"],
    ["w", "f", "f", "f", "w"],
    ["w", "j", "f", "j", "w"],
    ["w", "w", "e", "w", "w"],
]

# every map in the game, by name. main.py copies this so maps can change (items picked up etc) without breaking the originals
MAPS = {
    "lab": LAB_MAP,
    "ruins": RUINS_MAP,
    "highway": HIGHWAY_MAP,
    "hideout": HIDEOUT_MAP,
}

# how each map gets described in door messages, e.g. "*The way to the ruins."
MAP_NAMES = {
    "lab": "the lab",
    "ruins": "the ruins",
    "highway": "the highway",
    "hideout": "Twinkly's hideout",
}

# chance of a random battle each time the player steps onto a floor tile ("f"), per map
# maps not listed here (like the lab and the hideout) are safe
ENCOUNTER_RATES = {
    "ruins": 0.08,    # 8% per step
    "highway": 0.05,  # 5% per step
}

# every door in the game: (map, x, y) of the door -> (map it leads to, x, y the player arrives at)
# to add a new door, put an "e" on the map and add a line here
DOORS = {
    ("lab", 5, 1): ("ruins", 1, 2),
    ("lab", 5, 2): ("ruins", 1, 2),
    ("ruins", 0, 2): ("lab", 4, 2),
    ("ruins", 0, 3): ("lab", 4, 2),
    ("ruins", 5, 1): ("highway", 1, 1),
    ("ruins", 5, 2): ("highway", 1, 2),
    ("highway", 0, 1): ("ruins", 4, 1),
    ("highway", 0, 2): ("ruins", 4, 2),
    ("highway", 7, 2): ("hideout", 2, 3),
    ("hideout", 2, 4): ("highway", 6, 2),
}


def tile_code(grid, x, y):
    #returns the raw tile code (like 'w' or 'f') at a position on a grid
    return grid[y][x]


def is_encounter_tile(grid, x, y):
    #returns True if standing on this tile should start a battle
    code = tile_code(grid, x, y)
    return MAPBIOM[code]["encounter"]


def get_bounds(grid):
    #returns (max_x, max_y) which r the highest valid x and y positions
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1
    return max_x, max_y


def find_tile(grid, code):
    #finds the (x, y) of the first tile matching code, e.g. find_tile(LAB_MAP, 's')
    for row_index, row in enumerate(grid):
        for col_index, tile in enumerate(row):
            if tile == code:
                return col_index, row_index
    return None


def find_adjacent_tile(grid, x, y, code):
    # checks the 4 tiles around (x, y) for a tile matching code, returns its (x, y) or None
    # used for talking to npcs, since the player stands next to them, not on them
    max_x, max_y = get_bounds(grid)
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx <= max_x and 0 <= ny <= max_y and grid[ny][nx] == code:
            return nx, ny
    return None


def render_map(grid, player_x, player_y, follower_pos=None):

    #prints the map using each tile's art block instead of one character. For every row of tiles, build TILE_HEIGHT lines of text (one line per row of the block), gluing each tile's block onto those lines side
    #by side, then print those lines before moving to the next row of tiles

    for row_index, row in enumerate(grid):
        # start with TILE_HEIGHT empty strings, one for each line of this tile row
        lines = [""] * TILE_HEIGHT

        for col_index, code in enumerate(row):
            if col_index == player_x and row_index == player_y:
                block = PLAYER_ART
            elif follower_pos == (col_index, row_index):
                block = FOLLOWER_ART  # an ally walking one tile behind the player
            else:
                block = MAPBIOM[code]["art"]

            # add this tile's block onto the matching line
            for line_index in range(TILE_HEIGHT):
                lines[line_index] += block[line_index]

        for line in lines:
            print(line)
