# ohhh yeahh combat time babyyyy
# the actual battle system, FIGHT / ACT / ITEM / MERCY, shoutout toby fox
# start_battle() is the entry point everything else in here supports

import random
from enemies import spawn_enemies

# the things the player can do under act, check is always first, rename/add effects to the other two here later unless you wanna keep these as the default but why would you do that lmao
ACT_OPTIONS = ["Check", "Taunt", "Threaten"]

# reward ranges, fighting gives xp and platinum, sparing gives only platinum but more of it
# NOTE: these get rolled fresh inside start_battle each time you win, not here, random.randint() up here would only run once when the file loads and then every win for the rest of the game would give the exact same number which is stupid
# so don't change that because that would be stupid and stupid is bad
# and stupid
# very stupid

FIGHT_WIN_XP_RANGE = (5, 12)
FIGHT_WIN_PLATINUM_RANGE = (3, 7)
SPARE_WIN_PLATINUM_RANGE = (10, 15)


def enemy_display_name(enemy):
    # once an enemy can be spared put its name in ** ** everywhere I show it
    if enemy["spareable"]:
        return f"**{enemy['name']}**"
    return enemy["name"]


def start_battle(player, current_map):
    enemies = spawn_enemies()
    print("\n*A battle begins!*")
    for enemy in enemies:
        print(f"A {enemy['name']} appears!")

    while True:
        if not enemies:
            xp_gain = random.randint(*FIGHT_WIN_XP_RANGE)
            platinum_gain = random.randint(*FIGHT_WIN_PLATINUM_RANGE)
            print("\n*You won the battle!*")
            current_map[player.y][player.x] = "f"  # clear the tile, like items do
            player.xp += xp_gain
            player.platinum += platinum_gain
            print(f"*You gained {xp_gain} XP and {platinum_gain} platinum!*")
            break

        if not player.is_alive():
            print("\n*You have been defeated...*")
            break

        show_status(player, enemies)
        choice = input("\nFIGHT   ACT   ITEM   MERCY\n-> ").strip().lower()

        if choice in ("fight", "f"):
            do_fight(enemies)
        elif choice in ("act", "a"):
            do_act(enemies)
        elif choice in ("item", "i"):
            do_item(player)
        elif choice in ("mercy", "m"):
            result = do_mercy(player, enemies)
            if result == "spared":
                platinum_gain = random.randint(*SPARE_WIN_PLATINUM_RANGE)
                current_map[player.y][player.x] = "f"
                player.platinum += platinum_gain
                print(f"*You gained {platinum_gain} platinum!*")
                break
            elif result == "fled":
                break
            # "partial", "blocked", or "back" -> keep fighting, nothing else to do

        else:
            print("*...that's not one of the options.*")
            continue  # don't let enemies attack for an invalid choice

        # enemies get a turn after the player obvs
        if enemies and player.is_alive():
            enemy_turn(player, enemies)


def show_status(player, enemies):
    print(f"\n{player.name.title()} - HP: {player.health}/{player.maxhealth}")
    for enemy in enemies:
        print(f"{enemy_display_name(enemy)} - HP: {enemy['health']}")


def choose_enemy(enemies):
    # only asks if there's actually a choice to make
    if len(enemies) == 1:
        return enemies[0]

    print("\nWhich enemy?")
    for i, enemy in enumerate(enemies, start=1):
        print(f"{i}. {enemy_display_name(enemy)} (HP: {enemy['health']})")
    print("0. Back")

    choice = input("-> ").strip()
    if choice == "0":
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(enemies):
        return enemies[int(choice) - 1]

    print("*...that's not a valid choice.*")
    return None


def do_fight(enemies):
    target = choose_enemy(enemies)
    if target is None:
        return

    damage = random.randint(3, 6)
    target["health"] -= damage
    print(f"\n*You strike the {enemy_display_name(target)} for {damage} damage!*")

    if target["health"] <= 0:
        print(f"*The {enemy_display_name(target)} was destroyed!*")
        enemies.remove(target)


def do_act(enemies):
    target = choose_enemy(enemies)
    if target is None:
        return

    print("\n1. Check   2. Taunt   3. Threaten   0. Back")
    choice = input("-> ").strip()

    if choice == "1":
        print(f"\n*{enemy_display_name(target)} - HP: {target['health']}*")
        print(f"*{target['description']}*")
    elif choice == "2":
        target["spareable"] = True  # this is the "method" that makes it spareable
        print(f"\n*You taunt the {enemy_display_name(target)}. It seems ready to be spared.*")
    elif choice == "3":
        target["spareable"] = True  # this one too - either works
        print(f"\n*You threaten the {enemy_display_name(target)}. It seems ready to be spared.*")
    elif choice == "0":
        return
    else:
        print("*...that's not a valid choice.*")


def do_item(player):
    # weapons/armours use "" for an empty slot, so filter those out
    items = [w for w in player.weapons if w != ""] + [a for a in player.armours if a != ""]

    if not items:
        print("\nYou have no items!")
        return

    print("\nWhich item?")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")
    print("0. Back")

    choice = input("-> ").strip()
    if choice == "0":
        return
    if choice.isdigit() and 1 <= int(choice) <= len(items):
        print(f"\n*You use the {items[int(choice) - 1]}.*")
        # nothing actually happens yet, maybe hook up real item effects later?
    else:
        print("*...that's not a valid choice.*")


def do_mercy(player, enemies):
    # returns "spared" (everyone's gone), "partial" (some spared, fight continues), "fled", "blocked" (nobody was ready yet), or "back"
    print("\n1. Spare   2. Flee   0. Back")
    choice = input("-> ").strip()

    if choice == "1":
        ready = [enemy for enemy in enemies if enemy["spareable"]]

        if not ready:
            print("\n*They don't look ready to be spared yet.*")
            return "blocked"

        # spare everyone who was already ready
        for enemy in ready:
            print(f"\n*You spare the {enemy_display_name(enemy)}.*")
            enemies.remove(enemy)
            player.spares += 1

        # the rest get a 20% chance to also back down, having just seen it happen
        still_here = list(enemies)  # copy - about to remove from enemies below
        for enemy in still_here:
            if random.random() < 0.20:
                print(f"*Seeing the others spared, the {enemy['name']} backs down too!*")
                enemies.remove(enemy)
                player.spares += 1

        if not enemies:
            return "spared"
        else:
            print("\n*The rest are still ready to fight.*")
            return "partial"

    elif choice == "2":
        print("\n*You flee from the battle!*")
        return "fled"
    elif choice == "0":
        return "back"
    else:
        print("*...that's not a valid choice.*")
        return "back"


def enemy_turn(player, enemies):
    for enemy in enemies:
        damage = random.randint(1, enemy["attack"])
        player.take_damage(damage)
        print(f"*The {enemy_display_name(enemy)} attacks you for {damage} damage!*")


#the combat system has made me rethink my life choices.
