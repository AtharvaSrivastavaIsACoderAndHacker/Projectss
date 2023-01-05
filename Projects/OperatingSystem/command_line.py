import os
print ("Welcome To CommandLine")
print("This is your normal Terminal as all commands work here")

# You can execute this and enter your basic terminal commands, it's just your terminal but in python. Enjoy !!
while True:
    command = input("")
    if (command != 'exit'):
        print(os.system(command))
    else:
        break
