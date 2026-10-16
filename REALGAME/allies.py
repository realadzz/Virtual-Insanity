# allies
# party members that can join the player, like in deltarune
# each ally is just a dictionary, and combat.py gives them their own turn in battle

TWINKLY = {
    "name": "Twinkly",
    "maxhealth": 15,
    "health": 15,
    "heal_range": (4, 7),  # how much "Heal" restores
    # twinkly never attacks, he only heals or calms enemies, so he can't mess up the player's route and because hes a "pacifist" heh thats pretty funny its almost as if he isnt wait what
}


def create_twinkly():
    return dict(TWINKLY)


def is_up(ally):
    # an ally at 0 hp is knocked out: they skip their turns and enemies stop targeting them
    # they stay knocked out until healed (save points for now, healing items later)
    return ally["health"] > 0


def damage_ally(ally, amount):
    ally["health"] = max(ally["health"] - amount, 0)


def heal_ally(ally, amount):
    ally["health"] = min(ally["health"] + amount, ally["maxhealth"])
