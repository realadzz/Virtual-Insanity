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
}

# the character used to represent the player. If this shows up as a box or a question mark in the terminal, just keep the question mark or do like "P" or sum idk
PLAYER_SYMBOL = "𖨆"

PLAYER_ART = ["   ", " " + PLAYER_SYMBOL + " "]

LAB_MAP = [
    ["w", "w", "w", "w", "w", "w"],
    ["w", "d", "d", "d", "d", "e"],
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
    ["w", "r", "r", "r", "f", "w"],
    ["w", "w", "w", "w", "w", "w"],
]


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


def render_map(grid, player_x, player_y):

    #prints the map using each tile's art block instead of one character. For every row of tiles, we build TILE_HEIGHT lines of text (one line per row of the block), gluing each tile's block onto those lines side
    #by side, then print those lines before moving to the next row of tiles

    for row_index, row in enumerate(grid):
        # start with TILE_HEIGHT empty strings, one for each line of this tile row
        lines = [""] * TILE_HEIGHT

        for col_index, code in enumerate(row):
            if col_index == player_x and row_index == player_y:
                block = PLAYER_ART
            else:
                block = MAPBIOM[code]["art"]

            # add this tile's block onto the matching line
            for line_index in range(TILE_HEIGHT):
                lines[line_index] += block[line_index]

        for line in lines:
            print(line)
