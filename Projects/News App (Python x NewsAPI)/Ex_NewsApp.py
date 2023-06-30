from os import system
import requests as r
from bs4 import BeautifulSoup as b
system('cls')
import win32com.client as win


speaker = win.Dispatch("SAPI.SpVoice")


def indianNews():
      url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey=d405a85ac813496687660e9533513d14&language=en"
      response = r.get(url)
      data = response.json()
      
      if (speak := input("Do You Want Me To Speak The Headlines 1by1 ? [Y/n] : ") == 'Y'):
            op = True
      else:      
           op = False 
            
      for i,item in enumerate(data['articles'],start=1):
            print(print(str(i) + '. ' + item['title'] + '\n'))
            speaker.speak((str(i) + item['title'])) if op == True else ""



def searchNews(query):
      url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey=d405a85ac813496687660e9533513d14&language=en"
      response = r.get(url)
      data = response.json()
      
      if (speak := input("Do You Want Me To Speak The Headlines 1by1 ? [Y/n] : ") == 'Y'):
            op = True
      else:      
           op = False 
      
      for i,item in enumerate(data['articles'],start=1):
            print(print(str(i) + '. ' + item['title'] + '\n'))
            speaker.speak((str(i) + item['title'])) if op == True else ""




system("cls")
print('1. Indian Headlines')
print('2. Search News')
print('3. Weather')
print('4. Stocks')
print('5. Tech')
choice = int(input("Option : "))


if(choice == 1 or choice == 2 or choice == 3  or choice == 4  or choice == 5):
    print("")
else:
    raise ValueError("Enter Valid Integers Only !")

system("cls")
if(choice == 1):
    indianNews()
    
if(choice == 2):
      searchNews(query := input("Enter The Search Term : "))
      
if(choice == 3):
      searchNews(query :="weather")
      
if(choice == 4):
      searchNews(query :="stocks")
      
if(choice == 5):
      searchNews(query :="tech")