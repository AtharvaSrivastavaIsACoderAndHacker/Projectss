from os import system
import random



def game ():
            score = 0
            def incORdecrement (score,x):
                  if x == 0:
                        return score-1
                  elif x==1:
                        return score+1

            while True:
                  uIn = int(input("Your Turn : "))
                  comp = random.randint(0,2)
                  print("Computers Choosed : ",comp)


                  if uIn == comp:
                         print("Draw")
                         print("")
                  elif (uIn == 0 and comp == 1)or(uIn == 1 and comp == 2)or(uIn == 2 and comp == 0):
                         print("Lose")
                         print("")
                         score = incORdecrement(score,0)
                  elif (uIn == 1 and comp == 0)or(uIn == 2 and comp == 1)or(uIn == 0 and comp == 2):
                         print("Win")
                         print("")
                         score = incORdecrement(score,1)
                  elif uIn == 10:
                        system('cls')
                        print("Your Score Against Computer Is ",score)
                        break
                  else:
                        continue




system("cls")
print("Welcome To StonePaperSccissors !")
print("0 = Stone | 1 = Paper | 2 = Scissors | 10 = Exit The Game !")
startmsg = input("Press 'Enter Key To Starttttt !!!!!!")
system('cls') if startmsg == "" else ""
if startmsg == "":
       game()