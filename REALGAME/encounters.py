# encounters
# decides when a battle should start while the actual FIGHT/ACT/ITEM/MERCY system lives in combat.py, this file is just the trigger

from maps import is_encounter_tile
from combat import start_battle


def check_for_encounter(player, current_map):
    if is_encounter_tile(current_map, player.x, player.y):
        start_battle(player, current_map)
