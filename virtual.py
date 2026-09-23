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
print("My name is Adrian and I am the developer of this game. I really hope you enjoy. Now, let us begin.")


level = 1
maxhealth = 20
health = maxhealth
kills = 0
spares = 0
items = []
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
print("Try moving around. This can be done by inputting W, A, S or D.")


y=0
x=0
labmap = [["w","w","w","w","w","w"],
      ["w","d","d","d","d","e"],
      ["w","f","f","f","f","e"],
      ["w","s","g","f","f","w"],
      ["w","f","f","f","f","w"],
      ["w","f","d","d","d","w"],
      ["w","w","w","w","w","w"]]

y_len = len(map)-1
x_len = len(map)-1


print(y_len,x_len)
print(x,y)

mapbiom = {
   "w": {"t": "wall", "en": False},
   "e": {"t": "entrance", "en": False},
   "f": {"t": "floor", "en": False},
   "d": {"t": "desk", "en": False},
   "s": {"t": "start", "en": False},
   "g": {"t": "glass shard", "en": False},
}


current_tile = map(y)(x)
print(current_tile)
tilename=mapbiom[current_tile]["t"]
print(tilename)
entile=mapbiom[current_tile]["en"]
print(entile)

play = True
print("W - North/Up")
print("A - West/Left")
print("S - South/Down")
print("D - East/Right")
print("E - Interact")
print("-> means input movement")

while play == True:
   dest = input("-> ")
   current_tile = map(y)(x)
   tilename = mapbiom[current_tile]["t"]
   print(current_tile)
   print(x,y)
   if current_tile == "e":
       print("*There is a door here. It appears to be unlocked.")
   elif current_tile == "w":
       print("*There is a wall here.")
   elif current_tile == "d":
       print("*There are some desks here. They are all covered in dust, and have scattered papers all over.")
   elif current_tile == "g":
       glass_shard_choice = str(input("*There is a glass shard on the ground. Seems pretty good for self defence. \n Take it? \n *Yes    *No\n-> "))
       while glass_shard_choice.lower() == "":
           glass_shard_choice = input("*. . .")
       if glass_shard_choice.lower() == "yes":
           print("*You ate the moss. It was surprisingly very good. You gained all your health back!")
           health = maxhealth
       elif glass_shard_choice.lower() == "no":
           print("*You did not eat the moss. You feel like you just missed out on something truly great.")
           if health != 1:
               print(
                   "*In a way, you feel hurt by your own decisions.. (You took 1 damage..?")
               health -= 1
               print(health)
   if dest == "0":
       break
   elif dest.lower() == "w":
       if y > 0:
           y-= 1
   elif dest.lower() == "d":
       if x < x_len:
           x+= 1
   elif dest.lower() == "s":
       if y < y_len:
           y+= 1
   elif dest.lower() == "a":
       if x > 0:
           x-=1






