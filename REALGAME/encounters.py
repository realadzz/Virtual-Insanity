# encounters
# decides when a battle should start while the actual FIGHT/ACT/ITEM/MERCY system lives in combat.py, this file is just the trigger

import random
from maps import is_encounter_tile, tile_code, ENCOUNTER_RATES
from combat import start_battle


def check_for_encounter(player, current_map, current_map_name):
    # returns how the battle ended ("won", "spared", "fled", "dead"), or None if no battle happened

    # fixed encounters, like the robot corpse tiles
    if is_encounter_tile(current_map, player.x, player.y):
        return start_battle(player, current_map)

    # random encounters, only on plain floor so they don't happen on doors, items, save points etc
    rate = ENCOUNTER_RATES.get(current_map_name, 0)
    if tile_code(current_map, player.x, player.y) == "f" and random.random() < rate:
        return start_battle(player, current_map)

    return None
