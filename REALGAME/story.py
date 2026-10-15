# story stuff
# cutscenes and npc conversations live here so main.py doesn't turn into a novel and especially not a visual one ughhhh i hate visual novels except ddlc maybe

from combat import start_battle
from enemies import spawn_ambush_enemies
from allies import create_twinkly
from text import type_print

# on the tragedy route, the player needs to be at least this LV when they reach the ambush to be able to win it
TRAGEDY_AMBUSH_LV = 4


def narrate(text):
    # types a line out then waits for the player to press enter, so dialogue doesn't fly past
    type_print(text, end=" ")
    input()


def say(speaker, text):
    type_print(f'{speaker}: "{text}"', end=" ")
    input()


def is_tragedy_ambush(player):
    # tragedy route: only kills, no spares, and strong enough. twinkly never shows up
    return player.get_route() == "tragedy" and player.level >= TRAGEDY_AMBUSH_LV


def ambush(player):
    # the fight on the highway. returns how the battle ended
    # normally the player can't win this one and twinkly saves them ("rescued")
    # on the tragedy route it's a normal fight the player can win, and nobody comes
    tragedy = is_tragedy_ambush(player)
    print()
    narrate("*As you walk along the cracked highway, the ground starts to shake.")
    narrate("*Two machines burst out from under a flipped bus, their eyes glowing red.")
    if tragedy:
        narrate("*They hesitate for a moment when they see you.")
    else:
        narrate("*They don't look like they want to talk.")

    enemies = spawn_ambush_enemies(unbeatable=not tragedy)
    if tragedy:
        # they're scared of the player, so they're much easier to take down
        for enemy in enemies:
            enemy["health"] //= 2
    result = start_battle(player, None, enemies=enemies)

    if tragedy and result == "won":
        print()
        narrate("*The machines fall apart at your feet. They are now useless scraps, left to wither away for good.")
        narrate("*Nobody came to help..")
        narrate("*Nobody needed to.")
    return result


def rescue_cutscene(player):
    print()
    narrate("*Just as things start to look hopeless, a bright flash of light cuts through the air.")
    narrate("*A small android lands between you and the machines. Its round head glows like a star.")
    say("???", "Hey! Over here, you two! Bet you can't catch me!")
    narrate("*Another flash. The machines stumble, then collapse, twitching.")
    say("???", "That won't hold them for long. Come on, follow me! Quick!")
    narrate("*You follow the small android along the highway, until it slips through a crack in one of the huge concrete pillars.")
    narrate("*You squeeze in after it.")
    player.heal_full()
    print()


def twinkly_introduction(player):
    # only plays the first time the player talks to twinkly
    name = player.name.title()
    say("???", "Phew! We should be safe in here. Those two are way too big to fit through the gap.")
    say("???", "Oh! Where are my manners. I'm Twinkly, Twinkly the star!")
    say("Twinkly", "I used to light up the streets at night. Guide anyone who got lost, keep people safe... that kind of thing.")
    say("Twinkly", "Not that there's anyone left to guide nowadays..")
    say("Twinkly", "Anyway! Who are you? Where'd you come from? And why were you just strolling down the highway like that??")
    narrate("*You try to answer, but you can't remember anything.")
    narrate(f"*All you know is your name. {name}.")
    say("Twinkly", f"{name}, huh? And... that's it? Nothing else?")
    say("Twinkly", "Well, that's okay! Ask me whatever you want. I'll answer what I can.")


def talk_to_twinkly(player, flags):
    # the talkable npc menu. returns True once twinkly joins the party
    if not flags["met_twinkly"]:
        twinkly_introduction(player)
        flags["met_twinkly"] = True
    else:
        say("Twinkly", "Back already? What's up?")

    while True:
        print("\n 1. Who are you?")
        print(" 2. Where are we?")
        print(" 3. What's wrong with the machines?")
        print(" 4. Am I the only human left?")
        print(" 5. What do we do now?")
        print(" 0. Leave")
        choice = input("-> ").strip()
        print()

        if choice == "1":
            say("Twinkly", "Like I said, I'm Twinkly! A guardian android. Well... was. My job was keeping the city safe at night.")
            say("Twinkly", "I still try to do it, even if there's nobody around to protect anymore. Old habits!")
        elif choice == "2":
            say("Twinkly", "This is Tarnia! Or... what's left of it.")
            say("Twinkly", "It used to be the brightest city around. Hover-trains, holograms everywhere, robots for just about everything.")
            say("Twinkly", "Then the humans disappeared, and nature kind of... moved back in.")
        elif choice == "3":
            say("Twinkly", "The truth is, most machines out there aren't evil, they're just scared.")
            say("Twinkly", "With nobody left to fix them up, they'll do anything to keep running. Even scrap each other for parts.")
            say("Twinkly", "And lately, some of them have been acting... strange. Machines whisper about something called the Origin.")
            say("Twinkly", "Nobody really knows what it is. But it's nothing good, that's for sure.")
        elif choice == "4":
            narrate("*You ask Twinkly if you're the only human left.")
            say("Twinkly", "...")
            say("Twinkly", "Honestly? I don't know.")
            say("Twinkly", "I haven't seen a human in a long, long time. But hey, you're here, aren't you? So maybe there's hope!")
        elif choice == "5":
            say("Twinkly", "Hmm... you can't stay in here forever. And no offence, but you won't last long out there alone.")
            say("Twinkly", "So how about I come with you? I know these streets better than anyone!")
            say("Twinkly", "Besides... it's been a while since I had someone to look out for.")
            player.allies.append(create_twinkly())
            print("\n*Twinkly joined your party!*")
            print("*In battle, Twinkly can now heal you, or calm enemies down so they're easier to spare.*\n")
            return True
        elif choice == "0":
            say("Twinkly", "Take your time! I'm not going anywhere.")
            return False
        else:
            print("*...that's not one of the options.*")
