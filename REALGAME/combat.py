# ohhh yeahh combat time babyyyy
# the actual battle system, FIGHT / ACT / ITEM / MERCY, shoutout toby fox
# start_battle() is the entry point everything else in here supports

import random
from enemies import spawn_enemies
from allies import is_up, damage_ally, heal_ally
from text import type_print

# ACT options now live on each enemy in enemies.py (Check is always first, then that enemy's own acts)

# reward ranges, fighting gives xp and platinum, sparing gives only platinum but more of it
# NOTE: these get rolled fresh inside start_battle each time you win, not here, random.randint() up here would only run once when the file loads and then every win for the rest of the game would give the exact same number which is stupid
# so don't change that because that would be stupid and stupid is bad
# and stupid
# very stupid

FIGHT_WIN_XP_RANGE = (5, 12)
FIGHT_WIN_PLATINUM_RANGE = (3, 7)
SPARE_WIN_PLATINUM_RANGE = (10, 15)

# player damage, small range so it's consistent ish, but a crit can double it
# levelling up adds a bonus on top of this (see attack_bonus in player.py)
PLAYER_DAMAGE_RANGE = (4, 6)
CRIT_CHANCE = 0.10      # 10% chance
CRIT_MULTIPLIER = 2

# for unwinnable (scripted) fights: the battle gets interrupted once the player has
# taken this many turns, or their hp drops this low, whichever happens first
RESCUE_AFTER_TURNS = 4
RESCUE_AT_HP = 6


def enemy_display_name(enemy):
    # once an enemy can be spared put its name in ** ** everywhere game shows it
    if enemy["spareable"]:
        return f"**{enemy['name']}**"
    return enemy["name"]


def wake_up_allies(player):
    # after winning, knocked out allies get back up with 1 hp
    for ally in player.allies:
        if not is_up(ally):
            ally["health"] = 1
            type_print(f"*{ally['name']} slowly gets back up, barely holding together.*")


def start_battle(player, current_map, enemies=None):
    # returns how the battle ended: "won", "spared", "fled", "dead", or "rescued" (rescued is scripted fights only)
    # enemies can be passed in for special fights, otherwise random ones get spawned
    if enemies is None:
        enemies = spawn_enemies()
    scripted = any(enemy["unbeatable"] for enemy in enemies)
    turns_taken = 0

    type_print("\n*A battle begins!*")
    for enemy in enemies:
        type_print(f"A {enemy['name']} appears!")

    while True:
        if not enemies:
            xp_gain = random.randint(*FIGHT_WIN_XP_RANGE)
            platinum_gain = random.randint(*FIGHT_WIN_PLATINUM_RANGE)
            type_print("\n*You won the battle!*")
            if current_map is not None:
                current_map[player.y][player.x] = "f"  # clear the tile, like items do
            player.platinum += platinum_gain
            type_print(f"*You gained {xp_gain} XP and {platinum_gain} platinum!*")
            if player.gain_xp(xp_gain) > 0:
                type_print(f"*Your LV increased to {player.level}! Max HP is now {player.maxhealth}.*")
            wake_up_allies(player)
            return "won"

        if not player.is_alive():
            type_print("\n*GAME OVER*")
            return "dead"

        if scripted and (turns_taken >= RESCUE_AFTER_TURNS or player.health <= RESCUE_AT_HP):
            return "rescued"  # story.py takes over from here

        show_status(player, enemies)
        choice = input("\nFIGHT   ACT   ITEM   MERCY\n-> ").strip().lower()

        # each do_ function returns True if the player actually did something, or False if they backed out
        # (backing out of a menu doesn't use up the player's turn, like in undertale)
        if choice in ("fight", "f"):
            if not do_fight(player, enemies):
                continue
        elif choice in ("act", "a"):
            if not do_act(player, enemies):
                continue
        elif choice in ("item", "i"):
            if not do_item(player):
                continue
        elif choice in ("mercy", "m"):
            result = do_mercy(player, enemies)
            if result == "spared":
                platinum_gain = random.randint(*SPARE_WIN_PLATINUM_RANGE)
                if current_map is not None:
                    current_map[player.y][player.x] = "f"
                player.platinum += platinum_gain
                type_print(f"*You gained {platinum_gain} platinum!*")
                wake_up_allies(player)
                return "spared"
            elif result == "fled":
                return "fled"
            elif result == "back":
                continue
            # "partial" or "blocked" -> the player tried something, so the turn carries on

        else:
            print("*...that's not one of the options.*")
            continue  # don't let enemies attack for an invalid choice

        turns_taken += 1

        # allies get their turn after the player, like in deltarune (knocked out allies skip theirs)
        for ally in player.allies:
            if enemies and is_up(ally):
                ally_turn(ally, player, enemies)

        # enemies get a turn after the player obvs
        if enemies and player.is_alive():
            enemy_turn(player, enemies)


def show_status(player, enemies):
    # status uses normal print so it shows up instantly
    print(f"\n{player.name.title()} - LV {player.level} - HP: {player.health}/{player.maxhealth}")
    for ally in player.allies:
        if is_up(ally):
            print(f"{ally['name']} - HP: {ally['health']}/{ally['maxhealth']}")
        else:
            print(f"{ally['name']} - KNOCKED OUT")
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


def do_fight(player, enemies):
    target = choose_enemy(enemies)
    if target is None:
        return False

    damage = random.randint(*PLAYER_DAMAGE_RANGE) + player.attack_bonus()
    if random.random() < CRIT_CHANCE:
        damage *= CRIT_MULTIPLIER
        type_print("\n*CRITICAL HIT!*")

    target["health"] -= damage
    type_print(f"\n*You strike the {enemy_display_name(target)} for {damage} damage!*")

    if target["unbeatable"] and target["health"] <= 0:
        target["health"] = 1  # scripted enemies can't die
        type_print(f"*The {target['name']} shrugs off the hit like it was nothing.*")
    elif target["health"] <= 0:
        type_print(f"*The {enemy_display_name(target)} was destroyed!*")
        enemies.remove(target)
        player.kills += 1  # counts towards the route stuff
    return True


def do_act(player, enemies):
    target = choose_enemy(enemies)
    if target is None:
        return False

    # builds the menu from this enemy's own acts, e.g. "1. Check   2. Oil   3. Kick   0. Back"
    menu = "1. Check"
    for i, act in enumerate(target["acts"], start=2):
        menu += f"   {i}. {act['name']}"
    print("\n" + menu + "   0. Back")
    choice = input("-> ").strip()

    if choice == "0":
        return False
    if choice == "1":
        type_print(f"\n*{enemy_display_name(target)} - HP: {target['health']}  ATK: {target['min_attack']}-{target['max_attack']}*")
        type_print(f"*{target['description']}*")
        return True
    if not (choice.isdigit() and 2 <= int(choice) <= len(target["acts"]) + 1):
        print("*...that's not a valid choice.*")
        return False

    if target["unbeatable"]:
        type_print(f"\n*The {target['name']} doesn't even react. It isn't listening.*")
        return True

    act = target["acts"][int(choice) - 2]
    type_print(f"\n*{act['text']}*")

    if act.get("self_damage"):
        # an act can hurt, but it never kills the player, that would be a bit mean
        player.take_damage(min(act["self_damage"], player.health - 1))

    if act["spareable"] and not target["spareable"]:
        target["spareable"] = True
        type_print(f"*The {enemy_display_name(target)} seems ready to be spared.*")
    return True


def do_item(player):
    # weapons/armours use "" for an empty slot, so filter those out
    items = [w for w in player.weapons if w != ""] + [a for a in player.armours if a != ""]

    if not items:
        type_print("\nYou have no items!")
        return False

    print("\nWhich item?")
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")
    print("0. Back")

    choice = input("-> ").strip()
    if choice == "0":
        return False
    if choice.isdigit() and 1 <= int(choice) <= len(items):
        type_print(f"\n*You use the {items[int(choice) - 1]}.*")
        # nothing actually happens yet, maybe hook up real item effects later?
        return True
    print("*...that's not a valid choice.*")
    return False


def do_mercy(player, enemies):
    # returns "spared" (everyone's gone), "partial" (some spared, fight continues), "fled", "blocked" (nobody was ready yet), or "back"
    print("\n1. Spare   2. Flee   0. Back")
    choice = input("-> ").strip()

    if choice == "1":
        ready = [enemy for enemy in enemies if enemy["spareable"]]

        if not ready:
            type_print("\n*They don't look ready to be spared yet.*")
            return "blocked"

        # spare everyone who was already ready
        for enemy in ready:
            type_print(f"\n*You spare the {enemy_display_name(enemy)}.*")
            enemies.remove(enemy)
            player.spares += 1

        # the rest get a 20% chance to also back down, having just seen it happen
        still_here = list(enemies)  # copy - about to remove from enemies below
        for enemy in still_here:
            if not enemy["unbeatable"] and random.random() < 0.20:
                type_print(f"*Seeing the others spared, the {enemy['name']} backs down too!*")
                enemies.remove(enemy)
                player.spares += 1

        if not enemies:
            return "spared"
        else:
            type_print("\n*The rest are still ready to fight.*")
            return "partial"

    elif choice == "2":
        if any(enemy["unbeatable"] for enemy in enemies):
            type_print("\n*You try to run, but they cut you off!*")
            return "blocked"
        type_print("\n*You flee from the battle!*")
        return "fled"
    elif choice == "0":
        return "back"
    else:
        print("*...that's not a valid choice.*")
        return "back"


def ally_turn(ally, player, enemies):
    # an ally's turn, the player picks what they do just like in deltarune whatt deltarune by tobias henry thomas fox??
    print(f"\n{ally['name'].upper()}'S TURN")
    print("1. Heal   2. Shine   0. Skip")
    choice = input("-> ").strip()

    if choice == "1":
        print("\nHeal who?")
        print(f"1. {player.name.title()} ({player.health}/{player.maxhealth})")
        print(f"2. {ally['name']} ({ally['health']}/{ally['maxhealth']})")
        target = input("-> ").strip()
        amount = random.randint(*ally["heal_range"])
        if target == "2":
            heal_ally(ally, amount)
            type_print(f"\n*{ally['name']} tightens a few of his own bolts. He recovers {amount} HP!*")
        else:
            player.heal(amount)
            type_print(f"\n*{ally['name']} patches you up. You recover {amount} HP!*")
    elif choice == "2":
        target = choose_enemy(enemies)
        if target is None:
            return
        if target["unbeatable"]:
            type_print(f"\n*{ally['name']} shines a calming light, but the {target['name']} ignores it.*")
        else:
            target["spareable"] = True
            type_print(f"\n*{ally['name']} shines a calming light on the {enemy_display_name(target)}. It seems ready to be spared.*")
    else:
        type_print(f"\n*{ally['name']} waits.*")


def enemy_turn(player, enemies):
    for enemy in enemies:
        damage = random.randint(enemy["min_attack"], enemy["max_attack"])

        # each enemy picks someone to attack: the player, or any ally that's still standing
        targets = ["player"] + [ally for ally in player.allies if is_up(ally)]
        target = random.choice(targets)

        if target == "player":
            if enemy["unbeatable"]:
                damage = min(damage, player.health - 1)  # scripted fights can't kill the player so the thing doesnt bug out obviously
            player.take_damage(damage)
            type_print(f"*The {enemy_display_name(enemy)} attacks you for {damage} damage!*")
        else:
            damage_ally(target, damage)
            type_print(f"*The {enemy_display_name(enemy)} attacks {target['name']} for {damage} damage!*")
            if not is_up(target):
                type_print(f"*{target['name']} has been knocked out!*")


#the combat system has made me rethink my life choices.
#what am I getting myself into lmao
