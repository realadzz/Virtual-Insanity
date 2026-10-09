#MAIN FILE ADRIAN REMEMBER
# This is the file you actually run. It imports the pieces built in the other files and runs the main game loop.

from player import Player
from maps import LAB_MAP, RUINS_MAP, tile_code, get_bounds, find_tile, render_map
from items import pickup_glass_shard, pickup_blue_helmet
from encounters import check_for_encounter
from intro import print_intro, get_username


def print_controls():
    print("""
 ══ NAVIGATION ══════════════════════════════════════════
 ├─ MOVE   ►  [W] Up • [A] Left • [S] Down • [D] Right
 ├─ ACTION ►  [E] Interact / Enter Room
 └─ MENUS  ►  [Q] Inventory  │  [T] Stats Check
 ════════════════════════════════════════════════════════
""")


def move_player(player, direction, max_x, max_y):
    # moves player by a tile, assuming they're not blocked in that direction
    if direction == "w" and player.y > 0:
        player.y -= 1
    elif direction == "s" and player.y < max_y:
        player.y += 1
    elif direction == "a" and player.x > 0:
        player.x -= 1
    elif direction == "d" and player.x < max_x:
        player.x += 1


def handle_door(player, current_map_name, lab_visits):
    # handles what happens when the player interacts with a door
    if current_map_name == "lab":
        if lab_visits == 0:
            print("*There is a door here. It appears to be unlocked.")
        else:
            print("*The door to the ruins.")
    else:
        print("*The door to the lab.")

    choice = input("-> ")
    if choice.lower() != "e":
        # they didn't go through so nothing changes
        current_grid = LAB_MAP if current_map_name == "lab" else RUINS_MAP
        return current_grid, current_map_name, lab_visits

    if current_map_name == "lab":
        if lab_visits == 0:
            print("*You stepped out of the lab, and continued to walk around.")
            print("You look outside, finally getting a breath of fresh air. However... something is wrong.")
            print("Despite not remembering much, you remember there once being an amazing, flourishing city. You can't seem to remember its name though..")
            print("Regardless, this city is now different. It is destroyed, overrun by nature. Vines cling onto skyscrapers, flowers bloom on windows and you can smell the fresh air.")
        else:
            print("*You stepped back into the ruins.")
        player.x, player.y = 0, 2
        return RUINS_MAP, "ruins", lab_visits
    else:
        print("*You stepped back into the lab.")
        player.x, player.y = 5, 1
        return LAB_MAP, "lab", lab_visits + 1


def describe_tile(code):
    if code == "w":
        print("*There is a wall here.")
    elif code == "d":
        print("*There are some desks here. They are all covered in dust, and have scattered papers all over. They seem to be unimportant.")
    elif code == "r":
        print("*You notice a bunch of robots under some debris. They appear to be defunct..")


def run_game():
    print_intro()
    username = get_username()
    player = Player(username)

    current_map = LAB_MAP       # the grid we're walking on
    current_map_name = "lab"    # just a plain string
    lab_visits = 0

    # Put the player on the "s" (start) tile instead of always (0, 0)
    player.x, player.y = find_tile(current_map, "s")

    glass_shard_taken = False
    blue_helmet_taken = False

    print("You decide to explore, and try to understand what is going on.")
    print("Try moving around. The controls are listed below: ")
    print_controls()

    while True:
        move = input("-> ").lower()

        if move == "0":
            break

        max_x, max_y = get_bounds(current_map)
        move_player(player, move, max_x, max_y)

        code = tile_code(current_map, player.x, player.y)
        render_map(current_map, player.x, player.y)

        if code == "g" and not glass_shard_taken:
            glass_shard_taken = pickup_glass_shard(player)
            if glass_shard_taken:
                current_map[player.y][player.x] = "f"
        elif code == "bh" and not blue_helmet_taken:
            blue_helmet_taken = pickup_blue_helmet(player)
            if blue_helmet_taken:
                current_map[player.y][player.x] = "f"
        elif code == "e":
            current_map, current_map_name, lab_visits = handle_door(
                player, current_map_name, lab_visits
            )
        else:
            describe_tile(code)

        # after every move, check if the player stepped onto a tile that should start a battle. This is the "hook" between the movement system and the combat system.
        check_for_encounter(player, current_map)


if __name__ == "__main__":
    run_game()
