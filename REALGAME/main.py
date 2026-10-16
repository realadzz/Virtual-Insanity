#MAIN FILE ADRIAN REMEMBER
# This is the file players actually run as it imports the pieces built in the other files and runs the main game loop

import copy
import os

import time

from player import Player
from maps import (MAPS, MAP_NAMES, DOORS, BLOCKING_TILES, tile_code, get_bounds,
                  find_tile, find_adjacent_tile, render_map)
from items import PICKUPS, describe_pickup, take_pickup
from encounters import check_for_encounter
from intro import print_intro, get_username
from menus import show_inventory, show_stats
from story import ambush, rescue_cutscene, talk_to_twinkly, boss_fight, demo_ending, read_terminal
from shop import talk_to_vendy
from save import make_save, load_save, write_save_file, save_file_exists, read_save_file
from text import type_print

# clears the screen every time the player moves so old maps don't pile up
# (only works proper in cmd prompt or terminal so make false if its messing up)
CLEAR_SCREEN = True


def clear_screen():
    if CLEAR_SCREEN:
        os.system("cls" if os.name == "nt" else "clear")  # "cls" on windows


def print_controls():
    print("""
 ══ NAVIGATION ══════════════════════════════════════════
 ├─ MOVE   ►  [W] Up • [A] Left • [S] Down • [D] Right
 ├─ ACTION ►  [E] Interact / Enter Room
 └─ MENUS  ►  [Q] Inventory  │  [T] Stats Check  │  [0] Quit
 ════════════════════════════════════════════════════════
""")


def move_player(player, direction, grid):
    # moves the player by a tile, unless the map edge, a wall or an npc is in the way
    new_x, new_y = player.x, player.y
    if direction == "w":
        new_y -= 1
    elif direction == "s":
        new_y += 1
    elif direction == "a":
        new_x -= 1
    elif direction == "d":
        new_x += 1
    else:
        return  # not a movement key

    max_x, max_y = get_bounds(grid)
    if not (0 <= new_x <= max_x and 0 <= new_y <= max_y):
        return

    code = tile_code(grid, new_x, new_y)
    if code in BLOCKING_TILES:
        if code == "w":
            print("*There is a wall here.")
        elif code == "tw":
            print("*He is tinkering with some scrap. [E] to talk.")
        elif code == "sk":
            print("*An old vending machine. Its screen is blinking. [E] to talk.")
        elif code == "tm":
            print("*An old public terminal. [E] to read it.")
        elif code == "tr":
            print("*A tree, growing right through the pavement.")
        elif code == "gl":
            print("*GRIDLOCK towers over you. Its lights are stuck on red.")
        return

    player.x, player.y = new_x, new_y


def handle_door(player, current_map_name, flags):
    # handles what happens when the player steps on a door, returns the map the player ends up on
    destination = DOORS.get((current_map_name, player.x, player.y))
    if destination is None:
        type_print("*The door won't budge.")  # safety net in case a door was forgotten in DOORS
        return current_map_name
    dest_map, dest_x, dest_y = destination

    if dest_map == "hideout" and not flags["rescued"]:
        type_print("*There's a crack in one of the concrete highway pillars. It's pitch black inside.")
        type_print("*Something tells you not to go in alone.")
        return current_map_name

    if current_map_name == "lab" and not flags["left_lab"]:
        type_print("*There is a door here. It appears to be unlocked.")
    else:
        type_print(f"*The way to {MAP_NAMES[dest_map]}.")

    choice = input("-> ")
    if choice.lower() != "e":
        return current_map_name  # the player didn't go through so nothing changes

    if current_map_name == "lab" and not flags["left_lab"]:
        type_print("*You stepped out of the lab.")
        type_print("You look outside, finally getting a breath of fresh air. However... something is wrong.")
        type_print("Despite not remembering much, you remember there once being an amazing, flourishing city. You can't seem to remember its name though..")
        type_print("Regardless, this city is now different. It is destroyed, overrun by nature. Vines cling onto skyscrapers, flowers bloom on windows and the scent of flowers fills the air.")
        flags["left_lab"] = True
    else:
        type_print(f"*You head to {MAP_NAMES[dest_map]}.")

    # first time reaching the crossroads, describe the place
    if dest_map == "crossroads" and not flags["seen_crossroads"]:
        type_print("*You climb up a broken off-ramp and find yourself at an old crossroads.")
        type_print("*To the left, a shop sign flickers. To the right, trees have taken over a park.")
        type_print("*Straight ahead, something huge is blinking red.")
        flags["seen_crossroads"] = True

    player.x, player.y = dest_x, dest_y
    return dest_map


def describe_tile(code):
    if code == "d":
        type_print("*There are some desks here. They are all covered in dust, and have scattered papers all over. They seem to be unimportant.")
    elif code == "r":
        type_print("*You notice a bunch of robots under some debris. They appear to be defunct..")
    elif code == "c":
        type_print("*A car, rusted and crushed flat. Moss is growing out of the steering wheel, and vines cover the wheels.")
    elif code == "j":
        type_print("*A pile of scrap. Wires, bolts, a cracked screen. Nothing useful.")
    elif code == "bs":
        type_print("*An old crosswalk. Nobody's stopping you from crossing anymore.")


def draw(world, current_map_name, player, clear=False):
    # redraws the current map, with the following ally (if there is one) one step behind the player
    if clear:
        clear_screen()
    render_map(world[current_map_name], player.x, player.y, player.follower_pos)


def use_save_point(player, world, current_map_name, flags):
    # heals everyone, then saves (in memory AND to the save file). returns the new save
    player.heal_full()
    for ally in player.allies:
        ally["health"] = ally["maxhealth"]  # also brings knocked out allies back
    save = make_save(player, world, current_map_name, flags)

    type_print("*The thought of finding out the truth keeps you going.")
    try:
        write_save_file(save)
        if player.allies:
            type_print("*Your whole party's HP was fully restored. Progress saved.")
        else:
            type_print("*HP fully restored. Progress saved.")
    except OSError:
        # e.g. the folder is read-only. the game still works, it just can't save to a file
        type_print("*HP fully restored. (Couldn't write the save file, progress only saved until the game closes.)")
    return save


def default_flags():
    # anything that only happens once goes in here
    # (picked up items don't need flags, the item tile just turns into floor once it's taken)
    return {
        "left_lab": False,
        "ambush_done": False,   # true once the highway ambush is over (on any route)
        "rescued": False,       # true once twinkly saves the player from the ambush
        "met_twinkly": False,   # true once twinkly's introduction has played
        "seen_crossroads": False,
        "met_vendy": False,
        "boss_done": False,     # true once gridlock is beaten or spared
    }


def start_new_game():
    print_intro()
    username = get_username()
    player = Player(username)

    # every map in one place, so saving/loading can copy them all at once
    world = copy.deepcopy(MAPS)
    current_map_name = "lab"

    # Put the player on the "s" (start) tile instead of always (0, 0)
    player.x, player.y = find_tile(world[current_map_name], "s")

    type_print("You decide to explore, and try to understand what is going on.")
    type_print("Try moving around. The controls are listed below: ")
    return player, world, current_map_name, default_flags()


def continue_game():
    # returns the loaded game, or None if there's no usable save file
    if not save_file_exists():
        return None

    choice = input("A save file was found.\n [C] Continue   [N] New game\n-> ").strip().lower()
    if choice != "c":
        return None

    loaded = read_save_file()
    if loaded is None:
        type_print("*The save file seems to be broken... starting a new game instead.")
        return None

    player, world, current_map_name, flags = load_save(loaded)
    # if the game got updated with new flags since this save was made, add them in
    flags = {**default_flags(), **flags}
    type_print(f"*Welcome back, {player.name.title()}.")
    return player, world, current_map_name, flags


def run_game():
    game = continue_game()
    if game is None:
        game = start_new_game()
    player, world, current_map_name, flags = game

    # save in memory at the very start, so dying before finding a save point doesn't break anything
    save = make_save(player, world, current_map_name, flags)

    print_controls()
    draw(world, current_map_name, player)  # so the player can see where they are straight away

    while True:
        move = input("-> ").lower()
        current_map = world[current_map_name]

        if move == "0":
            type_print("*See you soon...")
            time.sleep(1)
            break
        elif move == "q":
            show_inventory(player)
            draw(world, current_map_name, player)
            continue  # menus don't count as moving
        elif move == "t":
            show_stats(player)
            draw(world, current_map_name, player)
            continue
        elif move == "e":
            # E only does something if the player is on or next to something they can interact with
            here = tile_code(current_map, player.x, player.y)
            twinkly_position = find_adjacent_tile(current_map, player.x, player.y, "tw")
            next_to_vendy = find_adjacent_tile(current_map, player.x, player.y, "sk") is not None
            next_to_terminal = find_adjacent_tile(current_map, player.x, player.y, "tm") is not None
            if here == "sp":
                save = use_save_point(player, world, current_map_name, flags)
            elif here in PICKUPS:
                if take_pickup(player, here):
                    current_map[player.y][player.x] = "f"  # the item's gone from the map once it's taken
            elif twinkly_position is not None:
                joined = talk_to_twinkly(player, flags)
                if joined:
                    tx, ty = twinkly_position
                    current_map[ty][tx] = "f"  # twinkly follows the player now, so he leaves his spot
                    player.follower_pos = (tx, ty)  # and starts following from where he was standing
                    type_print("*(Head back out to the highway, there's a way up to the north side of it now.)\n")
                draw(world, current_map_name, player)
            elif next_to_vendy:
                talk_to_vendy(player, flags)
                draw(world, current_map_name, player)
            elif next_to_terminal:
                read_terminal(player)
                draw(world, current_map_name, player)
            else:
                print("*There's nothing to interact with here.")
            continue

        old_position = (player.x, player.y)
        move_player(player, move, current_map)

        # if the player didn't actually move (typo, wall, map edge), don't
        # re-trigger whatever tile they're already standing on
        if (player.x, player.y) == old_position:
            continue

        # the following ally steps into the tile the player just left
        if player.allies:
            player.follower_pos = old_position

        code = tile_code(current_map, player.x, player.y)
        draw(world, current_map_name, player, clear=True)

        result = None  # how a battle ended this turn, if there was one

        if code in PICKUPS:
            describe_pickup(code)  # the player presses [E] to actually take it
        elif code == "sp":
            type_print("*A calming light shines before you. [E] to interact.")
        elif code == "e":
            new_map_name = handle_door(player, current_map_name, flags)
            if new_map_name != current_map_name:
                current_map_name = new_map_name
                player.follower_pos = None  # the ally catches up once the player takes a step
                draw(world, current_map_name, player)
        elif code == "am" and not flags["ambush_done"]:
            result = ambush(player)
            if result in ("rescued", "won", "spared"):
                flags["ambush_done"] = True
                # the ambush only happens once, so turn all its tiles back into floor
                for row in current_map:
                    for i, tile in enumerate(row):
                        if tile == "am":
                            row[i] = "f"
            if result == "rescued":
                rescue_cutscene(player)
                flags["rescued"] = True
                # twinkly takes the player straight to his hideout
                current_map_name = "hideout"
                player.x, player.y = 2, 3
                draw(world, current_map_name, player)
                result = None  # the rescue already redrew the map
        elif code == "bs" and not flags["boss_done"]:
            result = boss_fight(player)
            if result in ("won", "spared"):
                flags["boss_done"] = True
                gx, gy = find_tile(current_map, "gl")
                current_map[gy][gx] = "f"  # gridlock's gone (or stepped aside), so the way is clear
                demo_ending(player, result)
                draw(world, current_map_name, player)
                result = None  # already handled, don't redraw again below
        else:
            describe_tile(code)

        # after every move, check if the player stepped onto a tile that should start a battle. This is the "hook" between the movement system and the combat system
        if result is None and code not in ("am", "bs"):
            result = check_for_encounter(player, world[current_map_name], current_map_name)

        if result == "dead":
            type_print("\n*Everything begins to go dark...*")
            type_print("*But before it fully does, you wake up in front of the light..?*\n")
            player, world, current_map_name, flags = load_save(save)
            draw(world, current_map_name, player)
        elif result is not None:
            draw(world, current_map_name, player)  # show the map again once a fight is over


if __name__ == "__main__":
    run_game()
