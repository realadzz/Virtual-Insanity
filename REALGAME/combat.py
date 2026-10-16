# ohhh yeahh combat time babyyyy
# the actual battle system, FIGHT / ACT / ITEM / MERCY, shoutout toby fox
# start_battle() is the entry point everything else in here supports

import random
from enemies import spawn_enemies
from allies import is_up, damage_ally, heal_ally
from items import HEALING_ITEMS, item_name
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

# boss fights give way more, cause they're way harder
BOSS_XP_RANGE = (30, 40)
BOSS_PLATINUM_RANGE = (25, 35)
BOSS_SPARE_PLATINUM_RANGE = (35, 45)

# player damage, small range so it's consistent ish, but a crit can double it
# levelling up adds a bonus on top of this (see attack_bonus in player.py)
PLAYER_DAMAGE_RANGE = (4, 6)
CRIT_CHANCE = 0.10      # 10% chance
CRIT_MULTIPLIER = 2

# equipment specials (see EQUIPMENT in items.py)
SHORT_CIRCUIT_CHANCE = 0.30  # glass shard: 30% chance per hit to short circuit the enemy
SHORT_CIRCUIT_DAMAGE = 2     # damage the sparks do at the start of each of the enemy's turns
SHORT_CIRCUIT_TURNS = 3      # how many turns the sparks last
DEFLECT_CHANCE = 1 / 6       # blue helmet: 1 in 6 chance for an attack on the player to do nothing

# chance of an enemy dropping a healing item after the player wins or spares
# batteries are listed 3 times so they drop 3x more often than repair kits
ITEM_DROP_CHANCE = 0.25  # 25%
ITEM_DROPS = ["old_battery", "old_battery", "old_battery", "repair_kit"]

# for unwinnable (scripted) fights: the battle gets interrupted once the player has
# taken this many turns, or their hp drops this low, whichever happens first
RESCUE_AFTER_TURNS = 4
RESCUE_AT_HP = 6


def enemy_display_name(enemy):
    # once an enemy can be spared put its name in ** ** everywhere game shows it
    if enemy["spareable"]:
        return f"**{enemy['name']}**"
    return enemy["name"]


def the(enemy, capital=True):
    # "The Rusted Robot" / "the Rusted Robot", but named enemies like GRIDLOCK don't get a "the"
    name = enemy_display_name(enemy)
    if enemy.get("proper_name"):
        return name
    return ("The " if capital else "the ") + name


def maybe_drop_item(player):
    # after a win or a spare, there's a chance the player finds a healing item
    if random.random() < ITEM_DROP_CHANCE:
        item = random.choice(ITEM_DROPS)
        if player.add_item(item):
            name = item_name(item)
            article = "an" if name[0].lower() in "aeiou" else "a"  # "an Old Battery", "a Repair Kit"
            type_print(f"*Something was left behind. You found {article} {name}!*")


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
    boss_fight = any(enemy.get("boss") for enemy in enemies)  # checked now, cause the list is empty by the end
    turns_taken = 0

    type_print("\n*A battle begins!*")
    for enemy in enemies:
        if enemy.get("proper_name"):
            type_print(f"{enemy['name']} blocks the way!")
        else:
            type_print(f"A {enemy['name']} appears!")

    while True:
        if not enemies:
            xp_gain = random.randint(*(BOSS_XP_RANGE if boss_fight else FIGHT_WIN_XP_RANGE))
            platinum_gain = random.randint(*(BOSS_PLATINUM_RANGE if boss_fight else FIGHT_WIN_PLATINUM_RANGE))
            type_print("\n*You won the battle!*")
            if current_map is not None:
                current_map[player.y][player.x] = "f"  # clear the tile, like items do
            player.platinum += platinum_gain
            type_print(f"*You gained {xp_gain} XP and {platinum_gain} platinum!*")
            if player.gain_xp(xp_gain) > 0:
                type_print(f"*Your LV increased to {player.level}! Max HP is now {player.maxhealth}.*")
            maybe_drop_item(player)
            wake_up_allies(player)
            return "won"

        if not player.is_alive():
            type_print("\n*GAME OVER*")
            return "dead"

        if scripted and (turns_taken >= RESCUE_AFTER_TURNS or player.health <= RESCUE_AT_HP):
            return "rescued"  # story.py takes over from here

        show_status(player, enemies)
        # the player can type the number, the letter, or the whole word
        print("\n 1. [F] FIGHT   2. [A] ACT   3. [I] ITEM   4. [M] MERCY")
        choice = input("-> ").strip().lower()

        # each do_ function returns True if the player actually did something, or False if they backed out
        # (backing out of a menu doesn't use up the player's turn, like in undertale)
        if choice in ("1", "f", "fight"):
            if not do_fight(player, enemies):
                continue
        elif choice in ("2", "a", "act"):
            if not do_act(player, enemies):
                continue
        elif choice in ("3", "i", "item"):
            if not do_item(player):
                continue
        elif choice in ("4", "m", "mercy"):
            result = do_mercy(player, enemies)
            if result == "spared":
                platinum_gain = random.randint(*(BOSS_SPARE_PLATINUM_RANGE if boss_fight else SPARE_WIN_PLATINUM_RANGE))
                if current_map is not None:
                    current_map[player.y][player.x] = "f"
                player.platinum += platinum_gain
                type_print(f"*You gained {platinum_gain} platinum!*")
                maybe_drop_item(player)
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

        # status effects (like short circuit sparks) hurt enemies right before they attack
        apply_status_effects(player, enemies)

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
        sparks = " (short circuited)" if enemy.get("shorted", 0) > 0 else ""
        charging = " (CHARGING!)" if enemy.get("charging") else ""
        print(f"{enemy_display_name(enemy)} - HP: {enemy['health']}{sparks}{charging}")


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
    type_print(f"\n*You strike {the(target, False)} for {damage} damage!*")

    if target["unbeatable"] and target["health"] <= 0:
        target["health"] = 1  # scripted enemies can't die
        type_print(f"*{the(target)} shrugs off the hit like it was nothing.*")
    elif target["health"] <= 0:
        destroy_enemy(player, enemies, target)
    elif player.weapon_special() == "short_circuit" and random.random() < SHORT_CIRCUIT_CHANCE:
        # the glass shard's special: robots don't bleed, but they can short circuit
        target["shorted"] = SHORT_CIRCUIT_TURNS
        type_print(f"*The glass shard cuts into its wiring! {the(target)} starts sparking!*")
    return True


def destroy_enemy(player, enemies, enemy):
    type_print(f"*{the(enemy)} was destroyed!*")
    enemies.remove(enemy)
    player.kills += 1  # counts towards the route stuff


def apply_status_effects(player, enemies):
    # short circuit: a few damage at the start of each enemy turn, until it wears off
    for enemy in list(enemies):  # copy, since enemies can get destroyed while looping
        if enemy.get("shorted", 0) <= 0:
            continue
        enemy["shorted"] -= 1
        enemy["health"] -= SHORT_CIRCUIT_DAMAGE
        type_print(f"*Sparks burst out of {the(enemy, False)}! It takes {SHORT_CIRCUIT_DAMAGE} damage.*")

        if enemy["unbeatable"] and enemy["health"] <= 0:
            enemy["health"] = 1  # scripted enemies still can't die
        elif enemy["health"] <= 0:
            destroy_enemy(player, enemies, enemy)
        elif enemy["shorted"] == 0:
            type_print(f"*{the(enemy)} stops sparking.*")


def add_mercy(enemy):
    # counts one step towards sparing an enemy. most enemies only need 1, the boss needs more
    # returns True if this step made the enemy spareable
    if enemy["spareable"]:
        return False
    enemy["mercy"] = enemy.get("mercy", 0) + 1
    needed = enemy.get("mercy_needed", 1)
    if enemy["mercy"] >= needed:
        enemy["spareable"] = True
        type_print(f"*{the(enemy)} seems ready to be spared.*")
        return True
    type_print(f"*{the(enemy)} seems a little calmer... ({enemy['mercy']}/{needed})*")
    return False


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
        type_print(f"\n*{the(target)} doesn't even react. It isn't listening.*")
        return True

    act = target["acts"][int(choice) - 2]
    type_print(f"\n*{act['text']}*")

    if act.get("self_damage"):
        # an act can hurt, but it never kills the player, that would be a bit mean
        player.take_damage(min(act["self_damage"], player.health - 1))

    if act["spareable"]:
        add_mercy(target)
    return True


def choose_heal_target(player):
    # asks who to heal. returns "player", an ally, or None if the player backs out
    # if there are no allies there's nobody else to pick, so it skips the question
    if not player.allies:
        return "player"

    print("\nUse it on who?")
    print(f"1. {player.name.title()} ({player.health}/{player.maxhealth})")
    for i, ally in enumerate(player.allies, start=2):
        status = f"{ally['health']}/{ally['maxhealth']}" if is_up(ally) else "KNOCKED OUT"
        print(f"{i}. {ally['name']} ({status})")
    print("0. Back")

    choice = input("-> ").strip()
    if choice == "1":
        return "player"
    if choice.isdigit() and 2 <= int(choice) <= len(player.allies) + 1:
        return player.allies[int(choice) - 2]
    return None


def do_item(player):
    # healing items only. weapons and armour show up in the [Q] inventory instead
    if not player.items:
        type_print("\nYou have no items you can use!")
        return False

    print("\nWhich item?")
    for i, item in enumerate(player.items, start=1):
        print(f"{i}. {item_name(item)} (heals {HEALING_ITEMS[item]['heal']} HP)")
    print("0. Back")

    choice = input("-> ").strip()
    if not (choice.isdigit() and 1 <= int(choice) <= len(player.items)):
        if choice != "0":
            print("*...that's not a valid choice.*")
        return False

    index = int(choice) - 1
    item = HEALING_ITEMS[player.items[index]]
    target = choose_heal_target(player)
    if target is None:
        return False

    player.items.pop(index)  # used up
    if target == "player":
        player.heal(item["heal"])
        type_print(f"\n*{item['use_text']} You recover {item['heal']} HP!*")
    else:
        was_knocked_out = not is_up(target)
        heal_ally(target, item["heal"])
        if was_knocked_out:
            # healing items are the way to bring a knocked out ally back mid-battle
            type_print(f"\n*You use the {item['name']} on {target['name']}. He flickers back to life with {target['health']} HP!*")
        else:
            type_print(f"\n*You use the {item['name']} on {target['name']}. He recovers {item['heal']} HP!*")
    return True


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
            type_print(f"\n*You spare {the(enemy, False)}.*")
            enemies.remove(enemy)
            player.spares += 1

        # the rest get a 20% chance to also back down, having just seen it happen
        still_here = list(enemies)  # copy - about to remove from enemies below
        for enemy in still_here:
            if not enemy["unbeatable"] and random.random() < 0.20:
                type_print(f"*Seeing the others spared, {the(enemy, False)} backs down too!*")
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
        if any(enemy.get("boss") for enemy in enemies):
            type_print("\n*You try to run, but the exit is blocked! There's no running from this one.*")
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
            type_print(f"\n*{ally['name']} shines a calming light, but {the(target, False)} ignores it.*")
        else:
            type_print(f"\n*{ally['name']} shines a calming light on {the(target, False)}.*")
            add_mercy(target)
    else:
        type_print(f"\n*{ally['name']} waits.*")


def enemy_turn(player, enemies):
    for enemy in enemies:
        enemy["turns"] = enemy.get("turns", 0) + 1

        # charge attacks (the boss): one turn charging up, then a huge hit the turn after
        if enemy.get("charging"):
            enemy["charging"] = False
            charge_hit(player, enemy)
            continue
        if enemy.get("charge_every") and enemy["turns"] % enemy["charge_every"] == 0:
            enemy["charging"] = True
            type_print(f"*{enemy['charge_text']}*")
            type_print("*(It'll hit hard next turn... maybe heal up?)*")
            continue

        damage = random.randint(enemy["min_attack"], enemy["max_attack"])

        # each enemy picks someone to attack the player, or any ally that's still standing
        targets = ["player"] + [ally for ally in player.allies if is_up(ally)]
        target = random.choice(targets)

        if target == "player":
            # the blue helmet's special is sometimes the attack just bounces off this is so peak lol howd i do this
            if player.armour_special() == "deflect" and random.random() < DEFLECT_CHANCE:
                type_print(f"*{the(enemy)} attacks, but your Blue Helmet flashes blue! The attack bounces right off!*")
                continue

            damage = max(damage - player.defense(), 1)  # armour softens every hit, but a hit always does at least 1
            if enemy["unbeatable"]:
                damage = min(damage, player.health - 1)  # scripted fights can't kill the player so the thing doesnt bug out obviously
            player.take_damage(damage)
            type_print(f"*{the(enemy)} attacks you for {damage} damage!*")
        else:
            damage_ally(target, damage)
            type_print(f"*{the(enemy)} attacks {target['name']} for {damage} damage!*")
            if not is_up(target):
                type_print(f"*{target['name']} has been knocked out!*")


def charge_hit(player, enemy):
    # the big charged attack, always aimed at the player. armour still helps, and deflect can still save the player
    if player.armour_special() == "deflect" and random.random() < DEFLECT_CHANCE:
        type_print(f"*{the(enemy)} unleashes its attack... but your Blue Helmet flashes blue and it bounces right off!!*")
        return
    damage = max(random.randint(*enemy["charge_attack"]) - player.defense(), 1)
    player.take_damage(damage)
    type_print(f"*{the(enemy)} unleashes a massive blast of light! You take {damage} damage!*")


#the combat system has made me rethink my life choices.
#what am I getting myself into lmao
