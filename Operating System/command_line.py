import os
print ("Welcome To CommandLine")
print("This is your normal Terminal as all commands work here")


while True:
    command = input("")
    if (command != 'exit'):
        print(os.system(command))
    else:
        break
