# player stats
# this lists things like their stats, position, and simple actions (take damage, pick up items)

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

        self.x = 0
        self.y = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

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
