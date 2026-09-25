#print("""__     _____ ____ _____ _   _   _    _
#\ \   / /_ _|  _ \_   _| | | | / \  | |
#\ \ / / | || |_) || | | | | |/ _ \ | |
# \ V /  | ||  _ < | | | |_| / ___ \| |___
#__\_/  |___|_| \_\|_|  \___/_/__ \_\_____| __
#|_ _| \ | / ___|  / \  | \ | |_ _|_   _\ \ / /
#| ||  \| \___ \ / _ \ |  \| || |  | |  \ V /
#| || |\  |___) / ___ \| |\  || |  | |   | |
#|___|_| \_|____/_/   \_\_| \_|___| |_|   |_| : The game """)

print("Welcome to the world of Virtual Insanity, a game in which your choices matter")
print("My name is Adrian and I am the developer of this game. I really hope you enjoy. Now, let us begin.\n\n")

canmove = False
level = 1
maxhealth = 20
health = maxhealth
kills = 0
spares = 0
weapons = ["", "", "", "", "", "", "", ""]        #Weapons inventory system!!
armours = ["", "", "", "", "", "", "", ""]

#route == "neutral" --- I don't need this just yet, will be for later.



print("You slowly open your eyes, as a bright blue light flickers. You try to breath, yet you're unable to. A strange, thick fluid has seemingly filled them, and your time is running out.\n")
print("You try to look around, but your eyes burn whenever you open them. You try to move, but you appear to be contained in a large glass tube, a container of sorts.\n")
print("Gathering all the energy you have left, you make a small crack in the tube. The fluid begins to seep out, and you finally get your first breath. You break through the tube, just to seeminly be located inside a laboratory of sorts.\nYou are unable to remember what this place is, or how you even got here.")
print("You think deeply, but cannot seem to remember anything. You try to remember your name, but you fail to.\nYou try harder, looking through distorted memories and thoughts, until suddenly, you remember.\nYour name is...\n-> ")
username = str(input(""))
username = username.lower()


invalidname1 = str("VZYX")
invalidname2 = str("GASTER")


while username.lower() == "gaster":
  print("Error code 403: Please try a different name.")
  username = str(input(""))


while username.lower() == "vzyx":
  print(". . .")
  username = str(input(""))


print("..." + username + ". That's right. Your name is " + username + ".")




print("You feel like you should walk around, and try to understand what is going on.")
print("Try moving around. The controls are listed below: ")

y = 0
x = 0

labmap = [
    ["w", "w", "w", "w", "w", "w"],
    ["w", "d", "d", "d", "d", "e"],
    ["w", "f", "f", "f", "f", "e"],
    ["w", "s", "g", "f", "f", "w"],
    ["w", "f", "f", "f", "f", "w"],
    ["w", "f", "d", "d", "d", "w"],
    ["w", "w", "w", "w", "w", "w"]
]

ruinsmap = [
    ["w", "w", "w", "w", "w", "w"],
    ["w", "bh", "f", "r", "f", "e"],
    ["e", "f", "f", "f", "f", "e"],
    ["e", "f", "f", "f", "f", "w"],
    ["w", "f", "f", "f", "f", "w"],
    ["w", "r", "r", "r", "f", "w"],
    ["w", "w", "w", "w", "w", "w"]
]

labbacktotal = 0


y_len = len(labmap) - 1
x_len = len(labmap) - 1
current_map = labmap

print(y_len, x_len)
print(x, y)

mapbiom = {
    "w": {"t": "wall", "en": False, },
    "e": {"t": "entrance", "en": False},
    "f": {"t": "floor", "en": False},
    "d": {"t": "desk", "en": False},
    "s": {"t": "start", "en": False},
    "g": {"t": "glass shard", "en": False},
    "bh": {"t": "blue helmet", "en": False},
    "r": {"t": "robot corpse", "en": True},
}

current_tile = current_map[y][x]
print(current_tile)
tilename = mapbiom[current_tile]["t"]
print(tilename)
entile = mapbiom[current_tile]["en"]
print(entile)

play = True
print(
    """
 ══ NAVIGATION ══════════════════════════════════════════
 ├─ MOVE   ►  [W] Up • [A] Left • [S] Down • [D] Right
 ├─ ACTION ►  [E] Interact / Enter Room
 └─ MENUS  ►  [Q] Inventory  │  [T] Stat Check
 ════════════════════════════════════════════════════════
"""
)


glass_shard_takeable = True
blue_helmet_takeable = True

while play:
    canmove = True
    dest = input("-> ")
    current_tile = current_map[y][x]
    tilename = mapbiom[current_tile]["t"]
    if dest == "0":
        break
    elif dest.lower() == "w":
        if y > 0: y -= 1
    elif dest.lower() == "d":
        if x < (x_len - 1): x += 1
    elif dest.lower() == "s":
        if y < y_len: y += 1
    elif dest.lower() == "a":
        if x > 0: x -= 1
    current_tile = current_map[y][x]
    print(current_tile)
    print("x =", x, "y =", y)
    if current_tile == "w":
        print("*There is a wall here.")
    elif current_tile == "d":
        print("*There are some desks here. They are all covered in dust, and have scattered papers all over.")
    elif current_tile == "g":
        if glass_shard_takeable == True:
            glass_shard_choice = str(input("*There is a glass shard on the ground. It is somewhat shaped like a knife. \n Take it? \n *Yes *No\n-> "))
            while glass_shard_choice.lower() == "":
                glass_shard_choice = input("*. . .")
            if glass_shard_choice.lower() == "yes":
                print("*You picked up the glass shard. Hopefully you don't get a cut.")
                weapons[0] = "glass_shard"
                glass_shard_takeable = False
            elif glass_shard_choice.lower() == "no":
                print("*You did not pick up the glass shard.")
    elif current_tile == "e":
        if current_map == labmap:
            if labbacktotal == 0:
                print("*There is a door here. It appears to be unlocked.")
            else:
                print("*The door to the ruins.")
        elif current_map == ruinsmap:
            print("*The door to the lab.")
        labbacktotal = labbacktotal
        dest = input("-> ")
        if dest.lower() == "e":
            if current_map == labmap:
                current_map = ruinsmap
                if labbacktotal == 0:
                    print("*You stepped out of the lab, and continued to walk around.\nYou eventually found an exit, and made your way out of the building.")
                    print("You look outside, finally getting a breath of fresh air. However... something is wrong. Very, very wrong.")
                    print("Despite not remembering much, you remember there once being an amazing, once flourishing city. That city, however, is now different. It is destroyed, overrun by nature.\nYou wonder what happened here, and why this mysterious city is now like this.")
                else:
                    print("*You stepped back into the ruins.")
                x = 0
                y = 2
            else:
                current_map = labmap
                print("*You stepped back into the lab.")
                labbacktotal += 1
                x = 5
                y = 1
            y_len = len(current_map) - 1
            x_len = len(current_map) - 1
    if current_tile == "bh":
        if blue_helmet_takeable == True:
            blue_helmet_choice = input("*Behind some debris, you notice a half broken armour stand.\nYou notice a helmet that pulses blue when approaching it. Take it?\n *Yes *No\n-> ")
            while blue_helmet_choice.lower() == "":
                blue_helmet_choice = input("*. . .")
            if blue_helmet_choice.lower() == "yes":
                if health > 1:
                    print("*You picked up the blue helmet. You got stung by a little zap, but you're fine.")
                    health -= 1
                else:
                    print("*You picked up the blue helmet. You feel a weak force pushing it away from you, but the force stops soon after.")
                armours[0] = "blue_helmet"
                blue_helmet_takeable = False
            elif blue_helmet_choice.lower() == "no":
                print("*You left behind the blue helmet.")
    elif current_tile == "r":
        print("*You notice a bunch of robots under some debris. They all appear to be defunct.")