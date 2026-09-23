health = int(input("DEBUG HEALTH: "))
maxhealth = int(input("DEBUG MAX HEALTH: "))




y=0
x=0
map = [["w","e","e","e","e","e","e","e","w"],
      ["w","f","f","f","f","m","f","f","w"],
      ["w","f","f","f","f","f","f","f","w"],
      ["w","f","f","f","f","f","f","f","w"],
      ["w","f","f","sh","f","f","f","f","w"],
      ["w","f","f","f","f","sh","f","f","w"],
      ["w","f","f","f","f","f","f","sh","w"],
      ["w","sh","f","f","f","f","f","f","w"],
      ["w","w","w","l","l","l","w","w","w"]]


y_len = len(map)-1
x_len = len(map[0])-1


print(y_len,x_len)
print(x,y)


biom = {
   "w": {"t": "wall", "en": True},
   "e": {"t": "entrance", "en": False},
   "f": {"t": "floor", "en": True},
   "sh": {"t": "shop", "en": False},
   "l": {"t": "lab", "en": False},
   "m": {"t": "moss", "en": False},
}


current_tile = map[y][x]
print(current_tile)
tilename=biom[current_tile]["t"]
print(tilename)
entile=biom[current_tile]["en"]
print(entile)


play = True
print("W - North/Up")
print("A - West/Left")
print("S - South/Down")
print("D - East/Right")
print("E - Interact")
print("-> means input movement")


while play==True:
   dest = input("-> ")
   current_tile = map[y][x]
   tilename = biom[current_tile]["t"]
   print(current_tile)
   print(x,y)
   if current_tile == "sh":
       print("*There is a shop here.")
   elif current_tile == "w":
       print("*There is a wall here.")
   elif current_tile == "sh":
       print("*There appears to be some sort of shop here.. (Press E to enter.)")
   elif current_tile == "m":
       mosschoice = str(input("*There is some moss under a rock on the ground. \n Eat it? \n *Yes    *No\n"))
       while mosschoice == "":
           mosschoice = input("*. . .")
       if mosschoice.lower() == "yes":
           print("*You ate the moss. It was surprisingly very good. You gained all your health back!")
           health = maxhealth
       elif mosschoice.lower() == "no":
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
