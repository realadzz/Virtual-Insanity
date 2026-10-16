# the pricks that hate you
# enemy data and how enemies get spawned for a battle

import random

# the pool of enemies a battle can pull from, health/attack are just starting numbers so easy to tweak once I see how battles actually feel and when others test it
# enemies hit for a random number between min_attack and max_attack, so their damage is way more unpredictable than the player's
#
# "acts" are the ACT options for that enemy (Check is always added first automatically, so don't put it here)
#   "spareable": True means doing this act makes the enemy spareable
#   "self_damage" (optional) hurts the player when they do it, for acts that are a bad idea lol
ENEMY_TYPES = [
    {
        "name": "Rusted Robot",
        "health": 18,
        "min_attack": 1,
        "max_attack": 4,
        "description": "Its joints creak. It doesn't look too dangerous.",
        "acts": [
            {"name": "Oil", "spareable": True,
             "text": "You find some oil and rub it into its creaky joints. It lets out a happy whirr."},
            {"name": "Kick", "spareable": False,
             "text": "You kick its leg. It creaks angrily. That didn't help."},
        ],
    },
    {
        "name": "Sparking Drone",
        "health": 12,
        "min_attack": 1,
        "max_attack": 7,
        "description": "Loose wires spark dangerously every few seconds. Best not to touch them.",
        "acts": [
            {"name": "Insulate", "spareable": True,
             "text": "You carefully wrap a loose wire with some old tape. The sparking stops, and the drone calms down."},
            {"name": "Touch", "spareable": False, "self_damage": 2,
             "text": "You touch the wires. BZZT! You take 2 damage. What did you expect?"},
        ],
    },
    {
        "name": "Glitched Hologram",
        "health": 10,
        "min_attack": 2,
        "max_attack": 6,
        "description": "An old advert, still trying to sell something to nobody. It flickers in and out.",
        "acts": [
            {"name": "Buy", "spareable": True,
             "text": "You pretend to buy whatever it's selling. It glitches with joy. Its first customer in years!"},
            {"name": "Ignore", "spareable": False,
             "text": "You ignore the advert. It just gets louder and more annoying."},
        ],
    },
    {
        "name": "Cleaner Bot",
        "health": 22,
        "min_attack": 1,
        "max_attack": 3,
        "description": "It keeps sweeping the same spot of rubble. It seems annoyed you're making a mess.",
        "acts": [
            {"name": "Tidy", "spareable": True,
             "text": "You help sweep the rubble into a neat pile. The Cleaner Bot beeps gratefully."},
            {"name": "Make a mess", "spareable": False,
             "text": "You kick the rubble everywhere. The Cleaner Bot is FURIOUS."},
        ],
    },
]

# the two enemies from the highway ambush. on most routes the player isn't meant to win this fight
# "unbeatable" makes combat.py stop them from dying, being spared, or being fled from
AMBUSH_ENEMIES = [
    {
        "name": "Scrap Hound",
        "health": 40,
        "min_attack": 1,
        "max_attack": 3,
        "description": "A four-legged machine built from old car parts. It growls through a broken speaker.",
        "acts": [
            {"name": "Pet", "spareable": True,
             "text": "You slowly reach out and pat its metal head. Its growling turns into a broken purr."},
            {"name": "Bark", "spareable": False,
             "text": "You bark at it. It barks back, way louder. Not good."},
        ],
    },
    {
        "name": "Rogue Sentry",
        "health": 50,
        "min_attack": 1,
        "max_attack": 4,
        "description": "An old security unit. The only order it has left seems to be 'eliminate'.",
        "acts": [
            {"name": "Surrender", "spareable": True,
             "text": "You put your hands up. Its red targeting light dims to a calm yellow."},
            {"name": "Show ID", "spareable": False,
             "text": "You show it an ID card you definitely don't have. It doesn't buy it."},
        ],
    },
]


def make_enemy(template, unbeatable=False):
    enemy = dict(template)  # copy so each enemy tracks its own hp
    enemy["spareable"] = False  # becomes True once the right act is used on it
    enemy["unbeatable"] = unbeatable
    return enemy


def spawn_enemies():
    # 10% chance of 2 enemies, otherwise just 1
    enemy_count = 2 if random.random() < 0.10 else 1
    return [make_enemy(random.choice(ENEMY_TYPES)) for _ in range(enemy_count)]


def spawn_ambush_enemies(unbeatable=True):
    return [make_enemy(template, unbeatable=unbeatable) for template in AMBUSH_ENEMIES]
