# my program uses time.sleep() to remind the user to drink water every hour !!!!!!!!!!!!!!!!!!!!

from win11toast import toast
from win32com.client import Dispatch
import time
from os import system

system("cls")

def remind():      
      s = Dispatch('SAPI.Spvoice')
      s.speak('Drink Water Buddy')
      toast('Stay Hydrated !','Drink Water Buddy !', audio='ms-winsoundevent:Notification.Looping.Alarm')


j = 3600
      
while True:
      remind()
      time.sleep(j)