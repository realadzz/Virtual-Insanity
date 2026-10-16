# items
# handles the item pickups that happen when you step onto certain tiles
# each pickup is its own small function so when adding new items, just add a new function here instead of editing the main game loop

from text import type_print


def ask_yes_no():
    # keeps asking until the player types something
    choice = input("*Yes *No\n-> ")
    while choice.strip() == "":
        choice = input("*. . .\n-> ")
    return choice.lower()


def pickup_glass_shard(player):
    type_print("*There is a glass shard on the ground. It has the shape of a small blade.")
    type_print("*Take it?")
    if ask_yes_no() == "yes":
        type_print("*You picked up the glass shard. Try to not get a cut.")
        player.add_weapon("glass_shard")
        return True
    else:
        type_print("*You did not pick up the glass shard.")
        return False


def pickup_blue_helmet(player):
    type_print("*Behind some debris, you notice a broken dummy.")
    type_print("*On it is a broken blue helmet, pulsing with energy. Take it?")
    if ask_yes_no() == "yes":
        if player.health > 1:
            type_print("*You picked up the blue helmet. You got stung by a small zap, but you'll be fine.")
            player.take_damage(1)
        else:
            type_print("*You picked up the blue helmet. A weak force pushes you away, but stops soon after.")
        player.add_armour("blue_helmet")
        return True
    else:
        type_print("*You left behind the blue helmet.")
        return False

#aura
