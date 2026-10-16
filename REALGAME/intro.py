# game introoo
# only put it here so that main isn't too cluttered tbh

import sys

from text import type_print, type_input


def print_intro():
    type_print("Welcome to the world of Virtual Insanity, a game in which your choices matter.")
    type_print("My name is Ad and I am the developer of this game. I hope you enjoy. Now, let us begin.\n\n")
    type_print("Beep. Beep. Beep.")
    type_print("You open your eyes, as a bright blue light flickers. You try to breathe, yet you're unable to. A strange, thick fluid has filled them.. your time is running out.\n")
    type_print("Beep beep. Beep beep.")
    type_print("You try to look around, but your eyes burn whenever you open them. You try to move, but you seem to be trapped in some glass tube.\n")
    type_print("Beep beep beep. Beep beep beep. Bee-")
    type_print("Gathering all the energy you have left, you make a small crack in the tube. The fluid begins to seep out, and you finally get your first breath. You break through the tube, finding yourself in some sort of laboratory.\nYou can't remember where you are, or how you got here..\n")
    type_print("You think deeply, but still can't remember anything. You try to remember your name, but you fail to.\nYou try harder, looking through distorted memories and thoughts, until suddenly, you remember.\nYour name is...")


def get_username():
    invalid_names = ["gaster", "vzyx", "chara", "frisk"]

    username = input("-> ").lower()

    while username in invalid_names or username.strip() == "":
        if username == "gaster":
            sys.exit()  # game closes because gaster needs more feats
        elif username == "vzyx":
            type_print(". . .")
        elif username == "chara":
            type_print("Not the true name this time.")
        elif username == "frisk":
            type_print("No..")
        username = input("-> ").lower()

    type_print(f"...{username}. That's right. Your name is {username}.")
    return username
