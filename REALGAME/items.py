# items
# handles the item pickups that happen when you step onto certain tiles
# each pickup is its own small function so when adding new items, just add a new function here instead of editing the main game loop

def pickup_glass_shard(player):
    choice = input(
        "*There is a glass shard on the ground. It is somewhat shaped like a knife.\n"
        "Take it?\n*Yes *No\n-> "
    )
    while choice.strip() == "":
        choice = input("*. . .\n-> ")

    if choice.lower() == "yes":
        print("*You picked up the glass shard. Hopefully you don't get a cut.")
        player.add_weapon("glass_shard")
        return True
    else:
        print("*You did not pick up the glass shard.")
        return False


def pickup_blue_helmet(player):
    choice = input(
        "*Behind some debris, you notice a half broken armour stand.\n"
        "You notice a helmet that pulses blue when approaching it. Take it?\n"
        "*Yes *No\n-> "
    )
    while choice.strip() == "":
        choice = input("*. . .\n-> ")

    if choice.lower() == "yes":
        if player.health > 1:
            print("*You picked up the blue helmet. You got stung by a little zap, but you're fine.")
            player.take_damage(1)
        else:
            print("*You picked up the blue helmet. You feel a weak force pushing it away, but it stops soon after.")
        player.add_armour("blue_helmet")
        return True
    else:
        print("*You left behind the blue helmet.")
        return False

#aura