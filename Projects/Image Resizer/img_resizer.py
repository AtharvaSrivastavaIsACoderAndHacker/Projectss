
from PIL import Image 
from os import system

system("cls")

print("Use Forward Slashes Only !")
img = input("Image Path : ")
im = Image.open(f"{img}") 
 
system("cls")

width, height = im.size 
 
# left = 4
# top = height / 5
# right = 154
# bottom = 3 * height / 5
# im1 = im.crop((left, top, right, bottom))
print("Enter New IMG Dimensions (x,y)")
x = int(input("x : "))
y = int(input("y : "))

system("cls")
new = (x,y)
im = im.resize(new)
im.show() 