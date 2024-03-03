import curses
from curses import wrapper
import requests
import json
import time


def main(screen):
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    
    screen.addstr("Only 100% Accuracy Allowed ! One Mistake And You Are Done For !")
    screen.addstr("Press ENTER Right After You Have Typed The Last Letter Of The Test To Get Your Results !")
    
    
    # # Getting, parsing , editing and printing the text to type
    api = "https://api.api-ninjas.com/v1/loremipsum?paragraphs=1"
    body = (requests.get(api, headers={'X-Api-Key': 'FYJJDgFA9wk1rR0Noohq+g==VeMtFk4uDaQDabBQ'})).text
    parsed_json = json.loads(body)
    text = parsed_json["text"]
    text = text.split(" ")
    textStr = ""
    for y in range(45,54):
        textStr = textStr  +  (text[y]) + " "                    
    screen.addstr(3,1,textStr) 
        
        
        
    # Getting and printing user input    
    for i in range(1,len(textStr)+1):
        
        # Looping Condition for inputting and printing keys by the user !
        screen.refresh()
        key = screen.getkey()
        if (i==1):
            start_time = time.time()
        screen.addstr(4,i,f"{key}",curses.color_pair(2))
        screen.refresh()
        
        # Condition for checking errors and displaying results upon pressing ENTER !
        if (key != textStr[i-1]):
            if(key == '\n'):
                end_time = time.time()
                elapsedTime = end_time - start_time
                wpm = (10/int(elapsedTime))*60
                screen.addstr(8,1,f"WPM : {wpm}",curses.color_pair(2))
                screen.addstr(9,1,f"Time Taken : {int(elapsedTime)} Seconds",curses.color_pair(2))
                screen.refresh()
                continue
            screen.addstr(4,i,f"{key}",curses.color_pair(1))
            screen.refresh()
            screen.addstr(6,1,"Oops, You Made A Mistake ! Press Ctrl+C To Exit !")
            screen.refresh()
            key = screen.getkey()
            if (key == '^?'):
                exit()
        screen.refresh()
        
            
            
        
    screen.getkey()
    screen.refresh()
    
    
    
    
    
wrapper(main)

# https://www.youtube.com/watch?v=NpmFbWO6HPU