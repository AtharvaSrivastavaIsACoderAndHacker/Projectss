import pyautogui
from PIL import Image, ImageGrab
import time

def takeScreenshot():
    image = ImageGrab.grab()
    return image
    image.show()

def hit(key):
    pyautogui.keyDown(key)
    return

def isCollide(data):
    for i in range(250, 300):
        for j in range(410, 550):
            if data[i, j] < 100:
                hit('down')

                return

    for i in range(355, 420):
        for j in range(563, 650):
            if data[i, j] < 100:
                hit('up')
                return
    return

if __name__ == "__main__":
    time.sleep(3)
    print("Hey.. Dino game is about to start in 3 seconds")
    hit('up')    
    
    while True:
        image = ImageGrab.grab().convert('L')
        data = image.load()
        isCollide(data)
    
    # # Draw the rectangle for cactus
    # for i in range(355, 420):
    #     for j in range(563, 650):
    #         data[i, j] = 0
        
    # # Draw the rectangle for birds
    # for i in range(250, 300):
    #     for j in range(410, 550):
    #         data[i, j] = 171

    #     image.show()
    #     break