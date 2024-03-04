import pyttsx3
import time
import speech_recognition as s
from os import system
import wikipedia
import webbrowser
from AppOpener import open
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import *

# --------------------------------------------------------------------

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# https://youtu.be/Lp9Ftuq2sVI?t=1895

# --------------------------------------------------------------------

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def takeCommand():
    mySpeech = s.Recognizer()
    with s.Microphone() as source:
        system("cls")
        print("Listening...")
        mySpeech.pause_threshold = 0.8
        mySpeech.adjust_for_ambient_noise(source,duration=1)
        audio = mySpeech.listen(source)

        try:
            system("cls")
            print("Recognizing")
            query = mySpeech.recognize_google(audio, language="en-in")
            system("cls")
            print(query)
        except Exception as e:
            print(e)
            print("Say That Again !")
            return "none"
    return query
                    


def greet ():
    currentHour = int(time.strftime('%H'))
    if currentHour >= 0 and currentHour <= 11 :
        print('Good Morning Atharva !')
        speak('Good Morning Atharva !')
    elif currentHour >=12 and currentHour <= 16 :
        print('Good Afternoon Atharva !')
        speak('Good Afternoon Atharva !')
    elif currentHour >= 17 and currentHour <=21 :
        print('Good Evening Atharva !')
        speak('Good Evening Atharva !')
    else :
        print('Good Ninni')


def openInChrome(url):
    path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(path))
    webbrowser.get('chrome').open_new_tab(url)




# --------------------------------------------------------------------


if __name__ == '__main__':
    system("cls")
    greet()

    while True:
        query = takeCommand().lower()
        
        
        if "wikipedia" in query:
            try:    
                    speak("Searching Wikipedia...")
                    print("Searching Wikipedia...")
                    query = query.replace("wikipedia","")
                    results = wikipedia.summary(query, sentences=2)
                    print(results)
                    speak("Wikipedia say's, "+results)
            except Exception as e:
                speak("Sorry, but that's an invalid search query !")

        elif "open gsmarena" in query or "gsmarena" in query:
            openInChrome("gsmarena.com")
            
        elif "overflow" in query:
            openInChrome("stackoverflow.com")

        elif "open youtube" in query or "youtube" in query:
            open("youtube")

        elif "open zoom" in query or "zoom" in query:
            open("zoom")
            
        elif "code" in query:
            open("visual studio code")
            
        elif "open vmware" in query or "vmware" in query:
            open("vmware workstation pro")
            
        elif "open android studio" in query or "android studio" in query:
            open("android studio")
        
        elif "time" in query:
            propertime = "The Time Is,"+str(time.strftime('%H'))+"Hours and"+str(time.strftime('%M'))+"Minutes" 
            system("cls")
            print(str(time.strftime('%H:%M')))
            speak(propertime)
            
            
            
        elif "search google for" in query:
            searchQuery = query.replace("search", "",1)
            searchQuery = searchQuery.replace("google", "",1)
            searchQuery = searchQuery.replace("for", "",1)
            print(searchQuery)
            speak(f"Showing Results For - {searchQuery}")
            openInChrome(url := f"https://www.google.com/search?q={searchQuery}")
