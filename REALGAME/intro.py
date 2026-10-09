# game introoo
# only put it here so that main isn't too cluttered ig

def print_intro():
    print("Welcome to the world of Virtual Insanity, a game in which your choices matter.")
    print("My name is Ad and I am the developer of this game. I hope you enjoy. Now, let us begin.\n\n")
    print("You open your eyes, as a bright blue light flickers. You try to breathe, yet you're unable to. A strange, thick fluid has filled them.. your time is running out.\n")
    print("You try to look around, but your eyes burn whenever you open them. You try to move, but you seem to be trapped in some glass tube.\n")
    print("Gathering all the energy you have left, you make a small crack in the tube. The fluid begins to seep out, and you finally get your first breath. You break through the tube, finding yourself in some sort of laboratory.\nYou can't remember where you are, or how you got here..\n")
    print("You think deeply, but still can't remember anything. You try to remember your name, but you fail to.\nYou try harder, looking through distorted memories and thoughts, until suddenly, you remember.\nYour name is...\n-> ")


def get_username():
    invalid_names = ["gaster", "vzyx", "chara", "frisk"]

    username = input("").lower()

    while username in invalid_names:
        if username == "gaster":
            print("Error code 403: Please try a different name.")
        elif username == "vzyx":
            print(". . .")
        elif username == "chara":
            print("Not the true name this time.")
        elif username == "frisk":
            print("No..")
        username = input("").lower()

    print(f"...{username}. That's right. Your name is {username}.")
    return username
