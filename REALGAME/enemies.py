# the pricks that hate you
# enemy data and how enemies get spawned for a battle

import random

# the pool of enemies a battle can pull from, ealth/attack are just starting numbers so easy to tweak once I see how battles actually feel and when others test it
ENEMY_TYPES = [
    {
        "name": "Rusted Robot",
        "health": 12,
        "attack": 3,
        "description": "Its joints creak. It doesn't look too dangerous.",
    },
    {
        "name": "Sparking Drone",
        "health": 8,
        "attack": 4,
        "description": "Loose wires spark dangerously every few seconds. Best not to touch them.",
    },
]


def spawn_enemies():
    # 10% chance of 2 enemies, otherwise just 1
    enemy_count = 2 if random.random() < 0.10 else 1

    enemies = []
    for _ in range(enemy_count):
        template = random.choice(ENEMY_TYPES)
        enemy = dict(template)  # copy so each enemy tracks its own hp
        enemy["spareable"] = False  # becomes True once acted on enough in battle
        enemies.append(enemy)

    return enemies
