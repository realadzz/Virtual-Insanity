# game introoo
# only put it here so that main isn't too cluttered ig

def print_intro():
    print("Welcome to the world of Virtual Insanity, a game in which your choices matter")
    print("My name is Ad and I am the developer of this game. I really hope you enjoy. Now, let us begin.\n\n")
    print("You slowly open your eyes, as a bright blue light flickers. You try to breath, yet you're unable to. A strange, thick fluid has seemingly filled them, and your time is running out.\n")
    print("You try to look around, but your eyes burn whenever you open them. You try to move, but you appear to be contained in a large glass tube, a container of sorts.\n")
    print("Gathering all the energy you have left, you make a small crack in the tube. The fluid begins to seep out, and you finally get your first breath. You break through the tube, just to seeminly be located inside a laboratory of sorts.\nYou are unable to remember what this place is, or how you even got here.")
    print("You think deeply, but cannot seem to remember anything. You try to remember your name, but you fail to.\nYou try harder, looking through distorted memories and thoughts, until suddenly, you remember.\nYour name is...\n-> ")


def get_username():
    invalid_names = ["gaster", "vzyx"]

    username = input("").lower()

    while username in invalid_names:
        if username == "gaster":
            print("Error code 403: Please try a different name.")
        elif username == "vzyx":
            print(". . .")
        username = input("").lower()

    print(f"...{username}. That's right. Your name is {username}.")
    return username
