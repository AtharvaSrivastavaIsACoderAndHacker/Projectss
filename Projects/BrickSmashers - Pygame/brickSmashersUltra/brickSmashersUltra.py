import pygame
from os import system
from pygame.locals import *
import random
import os
import sys

system("cls")

def resource_path(relative_path):
    return relative_path

def preload_images():
    images = []
    for i in range(8):
        path = resource_path(f"assetsUltra/Images/{i}.jpg")
        image = pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), (window_width, window_height)
        )
        pygame.transform.smoothscale(image, (window_width, window_height))
        images.append(image)
    return images

def initializeBricks(WH, Rows):
    bricks = []
    y = 40
    for j in range(Rows):
        for i in range(35,window_width-40,WH[0]+9):
            bricks.append(pygame.Rect(i,y,WH[0],WH[1]))
        y+=WH[1]+9
    return bricks

def scale_images(images, window_width, window_height):
    return [pygame.transform.smoothscale(image, (window_width, window_height)) for image in images]

window_width = 600
window_height = 600

pygame.init()
gameWindow = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BrickSmashersUltra By AtharvaSrivastava")

window_rect = gameWindow.get_rect()
window_x = window_rect.x
window_y = window_rect.y



def main():
    global window_height
    global window_width
    exitGame = False
    clock = pygame.time.Clock()
    FPS = 120
    ballX = int(window_width - 10)/2
    ballY = int(window_height - 10)/2
    Right = False
    Left = False
    Up = False
    Down = False
    velocity = 3.5
    barX = int(window_width - 170)/2
    barY = window_height-30
    barRight = False
    barLeft = False
    GameOver = False
    start = False
    help = False
    bricks = initializeBricks([40,20], 6)
    bgi = 0
    frameCount = 0
    background_images = preload_images()
    interfaceColour = (0,0,0)
    GameOverImg = pygame.transform.scale(pygame.image.load(resource_path(f"assetsUltra/Images/gameOver.jpg")).convert_alpha(), (window_width, window_height))
    WonImage = pygame.transform.scale(pygame.image.load(resource_path(f"assetsUltra/Images/win.png")).convert_alpha(), (window_width, window_height))
    firstTime = True
    font = pygame.font.Font(None, 36)
    startMsg = font.render(f'Press SPACE to start !', True, interfaceColour)
    startXY = (int(window_width - startMsg.get_width())/2, ballY-50+(abs(barY-ballY)-10)/2)
    Won = False
    i = random.randint(0,1)
    gameSounds = {"break": pygame.mixer.Sound("assetsUltra/Sounds/brickBreak.wav"),
                "jump": pygame.mixer.Sound("assetsUltra/Sounds/jump.wav"),
                "won": pygame.mixer.Sound("assetsUltra/Sounds/win.mp3"),
                "lost": pygame.mixer.Sound("assetsUltra/Sounds/lost.mp3"),
                }
    mute = False
    
    
    gameWindow.fill((255,255,255))
    pygame.event.pump()
    while not exitGame:
        if not GameOver:
            event = None                            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True                
                elif event.type == pygame.KEYDOWN:
                    if (event.key == K_SPACE):
                        start = True
                    if (event.key == K_h):
                        help = True
                    if (event.key == K_m):
                        mute = not mute
                    if (event.key == 1073741903):
                        barRight = True
                    if (event.key == 1073741904):
                        barLeft = True
                    if (event.key == K_w):
                        window_height+=20
                        background_images = scale_images(background_images, window_width, window_height)
                        startXY = (int(window_width - startMsg.get_width())/2, ballY-50+(abs(barY-ballY)-10)/2)
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_s):
                        window_height-=20
                        background_images = scale_images(background_images, window_width, window_height)
                        startXY = (int(window_width - startMsg.get_width())/2, ballY-50+(abs(barY-ballY)-10)/2)
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_a):
                        window_width-=20
                        background_images = scale_images(background_images, window_width, window_height)
                        startXY = (int(window_width - startMsg.get_width())/2, ballY-50+(abs(barY-ballY)-10)/2)
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_d):
                        window_width+=20
                        background_images = scale_images(background_images, window_width, window_height)
                        startXY = (int(window_width - startMsg.get_width())/2, ballY-50+(abs(barY-ballY)-10)/2)
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_f):
                        if bgi != 0:
                            bgi-=1
                        elif bgi==0:
                            bgi = 8
                    if (event.key == K_j):
                        if bgi != 8:
                            bgi+=1
                        elif bgi==8:
                            bgi = 0
                elif event.type == pygame.KEYUP:
                    if event.key == K_h:
                        help = False
                    barLeft = False
                    barRight = False
                
            if bgi == 0:
                gameWindow.fill((255, 255, 255))
                interfaceColour = (0,0,0)
            elif bgi!=0:
                gameWindow.blit(background_images[bgi-1], (0, 0))
                interfaceColour = (255,255,255)
                
            pygame.draw.circle(gameWindow, interfaceColour, (ballX,ballY),10)
            pygame.draw.rect(gameWindow, interfaceColour, pygame.Rect(barX,barY,170,8))
            
            for brick in bricks:
                if brick.colliderect(pygame.Rect(ballX - 5, ballY - 5, 10, 10)):
                    if not mute:
                        gameSounds["break"].play()
                    bricks.remove(brick)
                    if abs(ballX - brick.left) <= 5 or abs(ballX - brick.right) <= 5:
                        Right = not Right
                        Left = not Left
                    elif abs(ballY - brick.top) <= 5 or abs(ballY - brick.bottom) <= 5:
                        Up = not Up
                        Down = not Down
                else:
                    pygame.draw.rect(gameWindow, interfaceColour, brick)
                  
                    
            if bricks == []:
                if not mute:
                        gameSounds["won"].play()
                Won = True
                GameOver = True


            if help:
                helpY = startXY[1]+30
                font = pygame.font.Font(None, 20)
                startMsg = font.render(f'h - hold for Help', True, interfaceColour)
                gameWindow.blit(startMsg, (int(window_width - startMsg.get_width())/2, helpY+10)) 
                startMsg = font.render(f'space - Start', True, interfaceColour)
                gameWindow.blit(startMsg, (int(window_width - startMsg.get_width())/2, helpY+25)) 
                startMsg = font.render(f'w,a,s,d - Adjust Window Size', True, interfaceColour)
                gameWindow.blit(startMsg, (int(window_width - startMsg.get_width())/2, helpY+40)) 
                startMsg = font.render(f'f/j - Change Backdrop', True, interfaceColour)
                gameWindow.blit(startMsg, (int(window_width - startMsg.get_width())/2, helpY+55)) 
                startMsg = font.render(f'Right/Left Arrow Keys - Move Bar', True, interfaceColour)
                gameWindow.blit(startMsg, (int(window_width - startMsg.get_width())/2, helpY+70)) 
                startMsg = font.render(f'm - Mute/Unmute', True, interfaceColour)
                gameWindow.blit(startMsg, (int(window_width - startMsg.get_width())/2, helpY+85)) 
            
            
            if not start:
                font = pygame.font.Font(None, 36)
                startMsg = font.render(f'Press SPACE to start !', True, interfaceColour)
                Down = True
                if i==0:
                    Right = True
                elif i==1:
                    Left = True
                if firstTime:
                    font = pygame.font.Font(None, 25)
                    helpMsg = font.render(f'Hold \'h\' for HelpMenu', True, interfaceColour)
                    gameWindow.blit(helpMsg, (int(window_width - helpMsg.get_width())/2, startXY[1]+25))
                gameWindow.blit(startMsg, (startXY[0],startXY[1])) 
                pygame.display.update()
                continue
            

            velocity+=0.0001


            if Right and Down:
                ballX += velocity
                ballY += velocity
            elif Left and Down:
                ballX -= velocity
                ballY += velocity
            elif Right and Up:
                ballX += velocity
                ballY -= velocity
            elif Left and Up:
                ballX -= velocity
                ballY -= velocity
            elif Right:
                ballX+=velocity
            elif Left:
                ballX-=velocity
            elif Up:
                ballY-=velocity
            elif Down:
                ballY+=velocity
                
            if (barX-10>window_x):     
                if barLeft:
                    barX-=6
            if (barX+180<window_x+window_width):     
                if barRight:
                    barX+=6
                
            if ballY<=window_y:
                Down = True
                Up = False
            if int(ballY+10)>window_y+window_height and not(ballX+7>barX and ballX-7<barX+170):
                if not mute:
                        gameSounds["lost"].play()
                Down = False
                Up = False
                Right = False
                Left = False
                GameOver = True
                GameOverImg = pygame.transform.scale(pygame.image.load(resource_path(f"assetsUltra/Images/gameOver.jpg")).convert_alpha(), (window_width, window_height))
            if ballY+10>=barY and ballX+7>barX and ballX-7<barX+170:
                Up = True
                Down = False
                if not mute:
                    gameSounds["jump"].play()
            if ballX<=window_x:
                Right = True
                Left = False
            if ballX>=window_x+window_width:
                Left = True
                Right = False
                          
        else: 
            gameWindow.fill((255,255,255))
            font = pygame.font.Font(None, 36)
            # score_text = font.render(f'Score: {Score*10}', True, (0,0,0))
            # HIscore = font.render(f'HI Score: {HI_Score*10}', True, (0,0,0))
            text = font.render(f'playAgain : ENTER', True, (255,255,255))
            # gameWindow.blit(score_text, (275, 315))
            # gameWindow.blit(HIscore, (275, 375))
            if Won:
                WonImage = pygame.transform.smoothscale(WonImage, (window_width, window_height))
                gameWindow.blit(WonImage, (0,0))
            else:
                gameWindow.blit(GameOverImg, (0,0))
            gameWindow.blit(text, (int(window_width - text.get_width())/2, 435)) 
            event = None                            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True                
                elif event.type == pygame.KEYDOWN:
                    if (event.key == K_RETURN or event.key == K_KP_ENTER):
                        GameOver = False
                        exitGame = False
                        clock = pygame.time.Clock()
                        FPS = 120
                        ballX = int(window_width - 10)/2
                        ballY = int(window_height - 10)/2
                        Right = False
                        Left = False
                        Up = False
                        Down = False
                        velocity = 3.5
                        barX = int(window_width - 170)/2
                        barY = window_height-30
                        barRight = False
                        barLeft = False
                        start = False
                        bricks = initializeBricks([40,20], 6)
                        firstTime = False
                        Won = False
                        i = random.randint(0,1)
        
        frameCount+=1
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

pygame.quit()
exit()