# menus
# the [Q] inventory and [T] stats screens kept here so main doesn't get cluttered

from items import HEALING_ITEMS, EQUIPMENT, item_name, equipment_summary
from text import type_print


def equipped_tag(player, item):
    # adds [EQUIPPED] next to whatever the player has on
    if item in (player.equipped_weapon, player.equipped_armour):
        return " [EQUIPPED]"
    return ""


def show_inventory(player):
    weapons = [w for w in player.weapons if w != ""]
    armours = [a for a in player.armours if a != ""]

    print("\n ══ INVENTORY ════════════════════")
    print("  WEAPONS")
    if weapons:
        for weapon in weapons:
            print(f"   - {item_name(weapon)} ({equipment_summary(weapon)}){equipped_tag(player, weapon)}")
    else:
        print("   (empty)")

    print("  ARMOUR")
    if armours:
        for armour in armours:
            print(f"   - {item_name(armour)} ({equipment_summary(armour)}){equipped_tag(player, armour)}")
    else:
        print("   (empty)")

    print("  ITEMS")
    if player.items:
        for item in player.items:
            print(f"   - {item_name(item)} (heals {HEALING_ITEMS[item]['heal']} HP)")
    else:
        print("   (empty)")
    print(" ═════════════════════════════════")

    # only offer equipping if the player actually has something to equip
    if weapons or armours:
        choice = input(" [1] Equip / unequip   [0] Back\n-> ").strip()
        if choice == "1":
            equip_menu(player, weapons + armours)
    print()


def equip_menu(player, gear):
    print("\nWhich one?")
    for i, item in enumerate(gear, start=1):
        print(f"{i}. {item_name(item)}{equipped_tag(player, item)}")
    print("0. Back")

    choice = input("-> ").strip()
    if not (choice.isdigit() and 1 <= int(choice) <= len(gear)):
        return

    item = gear[int(choice) - 1]
    info = EQUIPMENT[item]

    if item in (player.equipped_weapon, player.equipped_armour):
        # picking something that's already on takes it off
        if info["kind"] == "weapon":
            player.equipped_weapon = None
        else:
            player.equipped_armour = None
        type_print(f"*You took off the {info['name']}.")
        return

    if info["kind"] == "weapon":
        player.equipped_weapon = item
    else:
        player.equipped_armour = item
    type_print(f"*You equipped the {info['name']}. ({equipment_summary(item)})")
    if info["special_text"]:
        type_print(f"*{info['special_text']}.")


def show_stats(player):
    # route isn't shown on purpose cause like that would obvs ruin the surprise or wtv
    weapon = item_name(player.equipped_weapon) if player.equipped_weapon else "none"
    armour = item_name(player.equipped_armour) if player.equipped_armour else "none"

    print("\n ══ STATS ════════════════════════")
    print(f'  "{player.name.title()}"')
    print(f"  LV {player.level:<10} HP {player.health}/{player.maxhealth}")
    print(f"  ATK +{player.attack_bonus():<8} DEF {player.defense()}")
    print(f"  XP {player.xp:<10} NEXT {player.xp_to_next_level()}")
    print(f"  PLAT {player.platinum}")
    print(f"  KILLS {player.kills:<7} SPARES {player.spares}")
    print(f"  WEAPON {weapon}")
    print(f"  ARMOUR {armour}")
    for ally in player.allies:
        if ally["health"] > 0:
            print(f"  PARTY {ally['name']} - HP {ally['health']}/{ally['maxhealth']}")
        else:
            print(f"  PARTY {ally['name']} - KNOCKED OUT")
    print(" ═════════════════════════════════\n")
