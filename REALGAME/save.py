# saving
# two kinds of save:
#  1. a snapshot in memory (make_save / load_save), used when the player dies
#  2. a real file on the computer (savefile.json), so progress is still there after closing the game

import copy
import json
import os

from player import Player

# the save file goes in the same folder as the game's .py files
SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savefile.json")

# youtube tutorials are so gas

def make_save(player, world, current_map_name, flags):
    # a save is just a snapshot of everything that can change while playing
    # copy.deepcopy makes a fully separate copy, so changing the real player/maps
    # afterwards doesn't secretly change the save too
    return {
        "player": copy.deepcopy(player),
        "world": copy.deepcopy(world),
        "map_name": current_map_name,
        "flags": dict(flags),
    }


def load_save(save):
    # copy again on load, otherwise dying a second time would load an already-changed save
    return (
        copy.deepcopy(save["player"]),
        copy.deepcopy(save["world"]),
        save["map_name"],
        dict(save["flags"]),
    )


def write_save_file(save):
    # json can't store a Player object directly, so vars() turns it into a normal dictionary first
    data = {
        "player": vars(save["player"]),
        "world": save["world"],
        "map_name": save["map_name"],
        "flags": save["flags"],
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=2)


def save_file_exists():
    return os.path.exists(SAVE_FILE)


def read_save_file():
    # turns the file back into a save. returns None if the file is broken
    try:
        with open(SAVE_FILE) as file:
            data = json.load(file)

        player = Player(data["player"]["name"])
        for key, value in data["player"].items():
            setattr(player, key, value)  # copy every saved stat back onto the player
        if player.follower_pos is not None:
            player.follower_pos = tuple(player.follower_pos)  # json turns tuples into lists, so turn it back

        return {
            "player": player,
            "world": data["world"],
            "map_name": data["map_name"],
            "flags": data["flags"],
        }
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


# tysm random coding tutorials ily