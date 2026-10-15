# player stats
# this lists things like their stats, position, and simple actions (take damage, pick up items, level up)

MAX_LEVEL = 20
HEALTH_PER_LEVEL = 4  # max hp gained every level up


def xp_needed_for(level):
    # total xp needed to reach a level: LV2 = 10, LV3 = 30, LV4 = 60, LV5 = 100...
    return 5 * level * (level - 1)


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.maxhealth = 20
        self.health = self.maxhealth
        self.kills = 0
        self.spares = 0
        self.xp = 0
        self.platinum = 0  # the game's currency

        # 8 weapon/armour slots, empty string means an empty slot
        self.weapons = [""] * 8
        self.armours = [""] * 8

        # party members who've joined the player (see allies.py)
        self.allies = []
        # where the following ally is standing on the map, None means hidden (eg right after going through a door)
        self.follower_pos = None

        self.x = 0
        self.y = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal_full(self):
        self.health = self.maxhealth

    def heal(self, amount):
        # heals but never goes over max hp
        self.health = min(self.health + amount, self.maxhealth)

    def is_alive(self):
        return self.health > 0

    def attack_bonus(self):
        # extra damage from levelling up, +1 per level after LV1
        return self.level - 1

    def xp_to_next_level(self):
        if self.level >= MAX_LEVEL:
            return 0
        return xp_needed_for(self.level + 1) - self.xp

    def gain_xp(self, amount):
        # adds xp and levels up as many times as needed, returns how many levels were gained
        self.xp += amount
        levels_gained = 0
        while self.level < MAX_LEVEL and self.xp >= xp_needed_for(self.level + 1):
            self.level += 1
            self.maxhealth += HEALTH_PER_LEVEL
            self.health += HEALTH_PER_LEVEL  # levelling up also heals by the same amount
            levels_gained += 1
        return levels_gained

    def add_weapon(self, weapon_name):
        #puts a weapon in the first empty slot, returns True if fit
        for i in range(len(self.weapons)):
            if self.weapons[i] == "":
                self.weapons[i] = weapon_name
                return True
        return False  # inventory full

    def add_armour(self, armour_name):
        for i in range(len(self.armours)):
            if self.armours[i] == "":
                self.armours[i] = armour_name
                return True
        return False

    def get_route(self):
        # which route the player is on based on kills/spares (neutral, tragedy or blessed)
        # super basic for now, will tweak the rules once the game has more enemies
        if self.kills == 0 and self.spares > 0:
            return "blessed"
        elif self.kills > 0 and self.spares == 0:
            return "tragedy"
        else:
            return "neutral"
