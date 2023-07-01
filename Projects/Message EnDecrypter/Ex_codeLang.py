import os



def enco():
   strToEncode = input("Enter The Text To Be Encrypted :- ")
   if( len(strToEncode)<3 ):
       print(strToEncode[::-1])
   else:
      prefix = strToEncode[0]
      do = ((strToEncode[1:len(strToEncode)]+prefix).swapcase())[::-1]
      os.system("cls")
      print(do)





def deco():
   strToDecode = input("Enter The Text To Be Decrypted :- ")
   if( len(strToDecode)<3 ):
       print(strToDecode[::-1])
   else:
      do = strToDecode[::-1]
      doo = do.swapcase()
      suffix = doo[len(doo)-1]
      os.system("cls")
      print(suffix+(doo[0:len(strToDecode)-1]))
      




os.system("cls")
print('1. Encrypting')
print('2. Decrypting')
choice = int(input("Enter The Conversion Option :- "))


if(choice == 1 or choice == 2):
    print("")
else:
    raise ValueError("Only Integers 1 & 2 Are Valid !")

os.system("cls")
if(choice == 1):
    enco()
if(choice == 2):
    deco()