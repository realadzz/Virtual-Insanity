# shop
# vendy's shop. vendy is an old vending machine that somehow woke up and STILL just wants to sell stuff lmao
# prices are in platinum. to add something to the shop, just add a line to SHOP_STOCK

from items import HEALING_ITEMS, EQUIPMENT, item_name, equipment_summary
from story import narrate, say
from text import type_print

# (item, price). healing items can be bought as many times as the player wants,
# gear (weapons/armour) can only be bought once, then it shows as SOLD OUT
SHOP_STOCK = [
    ("old_battery", 10),
    ("repair_kit", 25),
    ("steel_pipe", 45),
    ("hard_hat", 40),
]


def owns(player, item):
    return item in player.weapons or item in player.armours


def stock_line(player, item, price):
    # one line of the shop menu, e.g. "Repair Kit (heals 15 HP) - 25 plat"
    if item in HEALING_ITEMS:
        return f"{item_name(item)} (heals {HEALING_ITEMS[item]['heal']} HP) - {price} plat"
    if owns(player, item):
        return f"{item_name(item)} ({equipment_summary(item)}) - SOLD OUT"
    return f"{item_name(item)} ({equipment_summary(item)}) - {price} plat"


def buy(player, item, price):
    if item in EQUIPMENT and owns(player, item):
        say("Vendy", "Sorry! That one's out of stock. You bought the last one, remember?")
        return
    if player.platinum < price:
        say("Vendy", "ERROR: INSUFFICIENT FUNDS. ...that means you're too broke, friend.")
        return

    if item in HEALING_ITEMS:
        added = player.add_item(item)
    elif EQUIPMENT[item]["kind"] == "weapon":
        added = player.add_weapon(item)
    else:
        added = player.add_armour(item)

    if not added:
        say("Vendy", "Your pockets are full! Use some of that stuff first.")
        return

    player.platinum -= price
    narrate(f"*CLUNK. A {item_name(item)} drops out of Vendy's slot.")
    say("Vendy", "THANK YOU FOR YOUR PURCHASE! Have a refreshing day!")
    if item in EQUIPMENT:
        type_print("*(Equip it from your inventory with [Q].)")


def shop_menu(player):
    while True:
        print(f"\n ══ VENDY'S ═══════  You have {player.platinum} plat")
        for i, (item, price) in enumerate(SHOP_STOCK, start=1):
            print(f" {i}. {stock_line(player, item, price)}")
        print(" 0. Back")
        choice = input("-> ").strip()

        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(SHOP_STOCK):
            item, price = SHOP_STOCK[int(choice) - 1]
            buy(player, item, price)
        else:
            print("*...that's not one of the options.*")


def vendy_introduction(player):
    # only plays the first time the player talks to vendy
    narrate("*The vending machine's screen flickers on. A cheerful jingle plays, way too loud.")
    if player.get_route() == "tragedy":
        # vendy has heard about what the player's been doing...
        say("Vendy", "W-WELCOME, VALUED CUSTOMER! P-please don't break me. Just take what you want. And pay. Please pay.")
    else:
        say("Vendy", "WELCOME, VALUED CUSTOMER! You're my first customer in... ERROR: DATE NOT FOUND.")
        say("Vendy", "Name's Vendy! I sell snacks! Well. I used to sell snacks. Now I sell whatever I can find lying around.")


def talk_to_vendy(player, flags):
    if not flags["met_vendy"]:
        vendy_introduction(player)
        flags["met_vendy"] = True
    else:
        say("Vendy", "Oh! You're back! My favourite customer! My only customer, but still!")

    while True:
        print("\n 1. Buy")
        print(" 2. Talk")
        print(" 0. Leave")
        choice = input("-> ").strip()

        if choice == "1":
            shop_menu(player)
        elif choice == "2":
            say("Vendy", "Business has been slow ever since the humans left. Machines don't really need snacks, you know?")
            say("Vendy", "Oh, and if you're heading north, watch out for GRIDLOCK. He controls the old intersection.")
            say("Vendy", "He's been stuck on the same traffic cycle for years. Doesn't let ANYONE cross. Very rude.")
        elif choice == "0":
            say("Vendy", "COME AGAIN SOON! Or don't! Actually please do!")
            return
        else:
            print("*...that's not one of the options.*")
