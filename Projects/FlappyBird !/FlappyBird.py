import pygame
import random
import os
from os import system
from pygame.locals import *

SCREENx,SCREENy = 336,635
root = pygame.init()
gameWindow = pygame.display.set_mode((SCREENx,SCREENy))
pygame.display.set_caption("Flappy Chidiya")

system("cls")

def welcomeScreen(exitWelcome):
    MSG = pygame.transform.scale(pygame.image.load("gallery/sprites/message.jpg").convert_alpha(),(SCREENx,SCREENy))
    gameWindow.blit(MSG, (0, 0))
    pygame.display.update()
    while not(exitWelcome):
        for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit()
                if (event.type == pygame.KEYDOWN):
                    if (event.key == 13 or event.key == pygame.K_SPACE):
                        main()
                        exitWelcome = True

def runningBase(BASE,groundX,groundY):
    gameWindow.blit(BASE, (groundX, groundY))


def randomPipesAB_YPosition(Offset):
    A = random.randint(-300,-40)
    v = int((635 * 0.85)-30)
    B = A+320+Offset
    list = [A, B]
    return list


def isCollide(x,y,Upper,Lower,playerMidPos,playerMidHeight,pipeMidPos):
    if (y<Upper[1]+320) and (abs((x+17)-pipeMidPos)<26):
        return True
    if (y>Lower[1]) and (abs((x+17)-pipeMidPos)<26):
        return True
    return False  



def main():
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)

    exitGame = False
    gameOver = False
    clock = pygame.time.Clock()
    FPS = 90
    gravity = 1.1
    acceleration = 0.06
    score = 0
    Offset = 160
    groundX = 0
    groundY = SCREENy * 0.8
    gameSounds = {"die": pygame.mixer.Sound("gallery/audio/die.wav"),
                    "hit": pygame.mixer.Sound("gallery/audio/hit.wav"),
                    "point": pygame.mixer.Sound("gallery/audio/point.wav"),
                    "swoosh": pygame.mixer.Sound("gallery/audio/swoosh.wav"),
                    "wing": pygame.mixer.Sound("gallery/audio/wing.wav")
                    }


    gameSprites = {}

    PipeXi = SCREENx+52
    gameSprites = {"player": pygame.image.load("gallery/sprites/bird.png").convert_alpha(),
                "pipes": (pygame.transform.rotate(pygame.image.load("gallery/sprites/pipe.png").convert_alpha(),180),
                          pygame.image.load("gallery/sprites/pipe.png").convert_alpha()),
                "background": pygame.image.load("gallery/sprites/background.png").convert_alpha(),
                "message": pygame.image.load("gallery/sprites/message.jpg").convert_alpha(),
                "base": pygame.image.load("gallery/sprites/base.png").convert_alpha()
                }
   
    system("cls")
    x = (SCREENx-10)/5
    y = (SCREENy-gameSprites["player"].get_height())/2
    if os.path.exists('hiscore.txt'):
        with open('hiscore.txt' , 'r') as f:
            HI_Score = int(f.read())
    else:
        HI_Score = 0
        f = open('hiscore.txt', 'w')
        f.write('0')
        f.close()
    
    
    
    while not(exitGame):
        if gameOver:  
            if (int(score)>HI_Score):
                HI_Score=int(score)
                with open('hiscore.txt' , 'w') as f:
                    f.write(str(HI_Score))
            gameWindow.fill(WHITE)
            bg = pygame.image.load('gallery/sprites/background.png')
            bg = pygame.transform.scale(bg,(SCREENx,SCREENy)).convert_alpha()
            gameWindow.blit(bg,(0,0))
            gameWindow.blit(gameSprites["base"], (0, groundY))
            font = pygame.font.Font(None, 36)
            GOmsg = font.render(f'Chidiya Mar Gayi LOL !', True, (0,0,0))
            score_text = font.render(f'Score: {(score*10)}', True, (0,0,0))
            HIscore = font.render(f'HI Score: {HI_Score*10}', True, (0,0,0))
            text = font.render(f'PlayAgain : ENTER', True, (0,0,0))
            gameWindow.blit(score_text, ((SCREENx-score_text.get_width())/2, 335))
            gameWindow.blit(HIscore, ((SCREENx-HIscore.get_width())/2, 375))
            gameWindow.blit(GOmsg, ((SCREENx-GOmsg.get_width())/2, 240))
            gameWindow.blit(text, ((SCREENx-text.get_width())/2, 415))
            pygame.display.update()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit()
                if (event.type == pygame.KEYDOWN):
                        if (event.key == 13):
                            gameOver = False
                            welcomeScreen(exitWelcome:=False)
        else:
            flapping = False
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exitGame = True
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                        # pygame.transform.rotate(gameSprites["player"],-30)
                        flapping = True
                        gameSounds["wing"].play()
                        gravity = 1.1
                        y-=75
                    

            bg = pygame.image.load('gallery/sprites/background.png')
            bg = pygame.transform.scale(bg,(SCREENx,SCREENy)).convert_alpha()
                        
            
            if not(flapping):
                # pygame.transform.rotate(gameSprites["player"],60)
                gravity+=acceleration
                y+=gravity
            
            
            groundX -= 2
            if groundX <= -55:
                groundX = 0
            
            gameWindow.blit(bg, (0, 0))
            
            
            
            if PipeXi == SCREENx+52:
                AupBdown = randomPipesAB_YPosition(Offset)
            
            UpperPipes = [PipeXi,AupBdown[0]]
            LowerPipes = [PipeXi,AupBdown[1]]
            
            PipeXi -= 2
            
            if 0<UpperPipes[0]<5:
                UpperPipes.append([PipeXi,AupBdown[0]])
                LowerPipes.append([PipeXi,AupBdown[1]])
            
            if UpperPipes[0]<(-gameSprites["pipes"][0].get_width()):
                del UpperPipes[0]
                del LowerPipes[0] 
                PipeXi = SCREENx+52
                AupBdown1 = randomPipesAB_YPosition(Offset)
                UpperPipes = [PipeXi,AupBdown1[0]]
                LowerPipes = [PipeXi,AupBdown1[1]]
            if (y<0):
                gameOver = True
                gameSounds["hit"].play()
            elif (y>groundY-gameSprites["player"].get_height()):
                gameOver = True
                gameSounds["hit"].play()

            playerMidPos = x + gameSprites["player"].get_width()/2
            playerMidHeight = y + gameSprites["player"].get_height()/2
            pipeMidPos = int(PipeXi) + int(gameSprites["pipes"][1].get_width()/2)
            if abs(playerMidPos-pipeMidPos) < 1:
                score+=1
                Offset-=1
                gameSounds["point"].play()
            
            if (isCollide(x,y,UpperPipes,LowerPipes,playerMidPos,playerMidHeight,pipeMidPos)):
                gameSounds["hit"].play()
                gameOver = True
            
                                 
            
          
            gameWindow.blit(gameSprites["pipes"][0], (UpperPipes[0], UpperPipes[1]))
            gameWindow.blit(gameSprites["pipes"][1], (LowerPipes[0], LowerPipes[1]))
            
            runningBase(gameSprites["base"], groundX, groundY)
            font = pygame.font.Font(None, 30)
            score_text = font.render(f'Score: {(score*10)}', True, (0,0,0))
            gameWindow.blit(score_text, (10, 10))
            HIscore = font.render(f'HI Score: {HI_Score*10}', True, (0,0,0))
            gameWindow.blit(HIscore, (10, 35))
            gameWindow.blit(gameSprites["player"], (x,y))
            clock.tick(FPS)
            pygame.display.update()
     
     
     
if __name__ == "__main__":
    system("cls")
    exitWelcome = False
    welcomeScreen(exitWelcome) 
     

pygame.quit()
exit()


# By Atharva Srivastava