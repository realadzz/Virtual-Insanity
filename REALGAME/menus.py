# menus
# the [Q] inventory and [T] stats screens kept here so main doesn't get cluttered


def pretty_item_name(item):
    # "glass_shard" -> "Glass Shard"
    return item.replace("_", " ").title()


def show_inventory(player):
    weapons = [w for w in player.weapons if w != ""]
    armours = [a for a in player.armours if a != ""]

    print("\n ══ INVENTORY ════════════════════")
    print("  WEAPONS")
    if weapons:
        for weapon in weapons:
            print(f"   - {pretty_item_name(weapon)}")
    else:
        print("   (empty)")

    print("  ARMOUR")
    if armours:
        for armour in armours:
            print(f"   - {pretty_item_name(armour)}")
    else:
        print("   (empty)")
    print(" ═════════════════════════════════\n")


def show_stats(player):
    # route isn't shown on purpose cause like that would obvs ruin the surprise or wtv
    print("\n ══ STATS ════════════════════════")
    print(f'  "{player.name.title()}"')
    print(f"  LV {player.level:<10} HP {player.health}/{player.maxhealth}")
    print(f"  XP {player.xp:<10} NEXT {player.xp_to_next_level()}")
    print(f"  PLAT {player.platinum}")
    print(f"  KILLS {player.kills:<7} SPARES {player.spares}")
    for ally in player.allies:
        if ally["health"] > 0:
            print(f"  PARTY {ally['name']} - HP {ally['health']}/{ally['maxhealth']}")
        else:
            print(f"  PARTY {ally['name']} - KNOCKED OUT")
    print(" ═════════════════════════════════\n")
