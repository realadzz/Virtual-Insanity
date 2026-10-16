# items
# everything about items: what healing items do, and the item tiles the player can pick up on the map
# picking up works like save points: step on the item to see what it is, then press [E] to take it (or just walk away to leave it)

from text import type_print

# healing items, usable in battle through ITEM. the key (like "old_battery") is what gets stored in the player's items list
HEALING_ITEMS = {
    "old_battery": {
        "name": "Old Battery",
        "heal": 8,
        "use_text": "You hold the old battery. A warm tingle runs through you.",
    },
    "repair_kit": {
        "name": "Repair Kit",
        "heal": 15,
        "use_text": "You use the repair kit to patch up your wounds.",
    },
}


# weapons and armour the player can equip. only the equipped weapon/armour does anything in battle
#   weapons: "attack" is extra damage on every hit
#   armour:  "defense" is how much less damage the player takes from each hit (a hit always does at least 1)
#   "special" is the item's special ability, combat.py checks for these by name
EQUIPMENT = {
    "glass_shard": {
        "name": "Glass Shard",
        "kind": "weapon",
        "attack": 2,
        "special": "short_circuit",
        "special_text": "Short Circuit: hits can send sparks through enemies, hurting them for a few turns",
    },
    "blue_helmet": {
        "name": "Blue Helmet",
        "kind": "armour",
        "defense": 1,
        "special": "deflect",
        "special_text": "Deflect: a 1 in 6 chance for an attack to bounce right off",
    },
    # these two are sold at vendy's shop. more raw stats, but no special ability, so it's a trade off
    "steel_pipe": {
        "name": "Steel Pipe",
        "kind": "weapon",
        "attack": 4,
        "special": None,
        "special_text": None,
    },
    "hard_hat": {
        "name": "Hard Hat",
        "kind": "armour",
        "defense": 2,
        "special": None,
        "special_text": None,
    },
}


def item_name(item):
    # "old_battery" -> "Old Battery", "glass_shard" -> "Glass Shard"
    if item in HEALING_ITEMS:
        return HEALING_ITEMS[item]["name"]
    if item in EQUIPMENT:
        return EQUIPMENT[item]["name"]
    return item.replace("_", " ").title()


def equipment_summary(item):
    # short description for menus, e.g. "ATK +2, Short Circuit"
    info = EQUIPMENT[item]
    if info["kind"] == "weapon":
        stat = f"ATK +{info['attack']}"
    else:
        stat = f"DEF +{info['defense']}"
    if info["special_text"] is None:
        return stat  # no special ability, just stats
    special_name = info["special_text"].split(":")[0]
    return f"{stat}, {special_name}"


# every item tile on the map. "see" is shown when the player steps on it, "take" when they press [E]
# "kind" is which part of the inventory it goes in: "weapon", "armour" or "item" (healing items)
PICKUPS = {
    "g": {
        "item": "glass_shard",
        "kind": "weapon",
        "see": ["*There is a glass shard on the ground. It has the shape of a small blade."],
        "take": "*You picked up the glass shard. Try to not get a cut.",
    },
    "bh": {
        "item": "blue_helmet",
        "kind": "armour",
        "see": ["*Behind some debris, you notice a broken dummy.",
                "*On it is a broken blue helmet, pulsing with energy."],
        "take": "*You picked up the blue helmet.",  # the zap gets added in take_pickup below
    },
    "hb": {
        "item": "old_battery",
        "kind": "item",
        "see": ["*An old battery is lying in the dirt. It still feels slightly warm."],
        "take": "*You picked up the Old Battery. It heals 8 HP.",
    },
    "hk": {
        "item": "repair_kit",
        "kind": "item",
        "see": ["*A dusty repair kit is wedged under some scrap. It looks unused."],
        "take": "*You picked up the Repair Kit. It heals 15 HP.",
    },
}


def describe_pickup(code):
    # runs when the player steps onto an item tile
    for line in PICKUPS[code]["see"]:
        type_print(line)
    type_print("*[E] to take it.")


def take_pickup(player, code):
    # runs when the player presses [E] on an item tile. returns True if it was picked up
    pickup = PICKUPS[code]

    if pickup["kind"] == "weapon":
        added = player.add_weapon(pickup["item"])
    elif pickup["kind"] == "armour":
        added = player.add_armour(pickup["item"])
    else:
        added = player.add_item(pickup["item"])

    if not added:
        type_print("*You can't carry any more of those.")
        return False

    type_print(pickup["take"])

    # if the player has nothing equipped in that slot yet, equip it straight away
    if pickup["kind"] == "weapon" and player.equipped_weapon is None:
        player.equipped_weapon = pickup["item"]
        type_print(f"*You equipped the {item_name(pickup['item'])}. ({equipment_summary(pickup['item'])})")
    elif pickup["kind"] == "armour" and player.equipped_armour is None:
        player.equipped_armour = pickup["item"]
        type_print(f"*You equipped the {item_name(pickup['item'])}. ({equipment_summary(pickup['item'])})")

    # the blue helmet zaps the player a bit when they pick it up
    if code == "bh":
        if player.health > 1:
            type_print("*You got stung by a small zap, but you'll be fine.")
            player.take_damage(1)
        else:
            type_print("*A weak force pushes you away, but stops soon after.")
    return True

#aura
