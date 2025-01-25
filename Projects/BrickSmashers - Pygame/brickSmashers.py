import pygame
from os import system
from pygame.locals import *
import random

window_width = 600
window_height = 600

pygame.init()
gameWindow = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BrickSmashers By AtharvaSrivastava")

system("cls")

window_rect = gameWindow.get_rect()
window_x = window_rect.x
window_y = window_rect.y

def initializeBricks(WH, Rows):
    bricks = []
    y = 40
    for j in range(Rows):
        for i in range(35,window_width-40,WH[0]+9):
            bricks.append(pygame.Rect(i,y,WH[0],WH[1]))
        y+=WH[1]+9
    return bricks

def main():
    global window_height
    global window_width
    exitGame = False
    clock = pygame.time.Clock()
    FPS = 120
    ballX = 290
    ballY = 290
    Right = False
    Left = False
    Up = False
    Down = False
    velocity = 3.5
    barX = 200
    barY = window_height-30
    barRight = False
    barLeft = False
    GameOver = False
    start = False
    help = False
    bricks = initializeBricks([40,20], 6)
    
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
                    if (event.key == 1073741903):
                        barRight = True
                    if (event.key == 1073741904):
                        barLeft = True
                    if (event.key == K_w):
                        window_height+=20
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_s):
                        window_height-=20
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_a):
                        window_width-=20
                        pygame.display.set_mode((window_width, window_height))
                    if (event.key == K_d):
                        window_width+=20
                        pygame.display.set_mode((window_width, window_height))
                elif event.type == pygame.KEYUP:
                    if event.key == K_h:
                        help = False
                    barLeft = False
                    barRight = False
                
            gameWindow.fill((255,255,255))
            pygame.draw.circle(gameWindow, (0,0,0), (ballX,ballY),10)
            pygame.draw.rect(gameWindow, (0,0,0), pygame.Rect(barX,barY,170,8))
            
            for brick in bricks:
                if brick.colliderect(pygame.Rect(ballX - 5, ballY - 5, 10, 10)):
                        bricks.remove(brick)
                        if abs(ballX - brick.left) <= 5 or abs(ballX - brick.right) <= 5:
                            Right = not Right
                            Left = not Left
                        elif abs(ballY - brick.top) <= 5 or abs(ballY - brick.bottom) <= 5:
                            Up = not Up
                            Down = not Down
                else:
                    pygame.draw.rect(gameWindow, (0,0,0), brick)



            if help:
                font = pygame.font.Font(None, 20)
                startMsg = font.render(f'h - hold for Help', True, (0,0,0))
                gameWindow.blit(startMsg, (175, 330)) 
                startMsg = font.render(f'space - Start', True, (0,0,0))
                gameWindow.blit(startMsg, (175, 345)) 
                startMsg = font.render(f'w,a,s,d - Adjust Window Size', True, (0,0,0))
                gameWindow.blit(startMsg, (175, 360)) 
                startMsg = font.render(f'Right/Left Arrow Keys - Move Bar', True, (0,0,0))
                gameWindow.blit(startMsg, (175, 375)) 
            
            
            if not start:
                font = pygame.font.Font(None, 36)
                startMsg = font.render(f'Press SPACE to start !', True, (0,0,0))
                gameWindow.blit(startMsg, (175, 215)) 
                pygame.display.update()
                Down = True
                i = random.randint(0,1)
                if i==0:
                    Right = True
                elif i==1:
                    Left = True
                continue

            velocity+=0.00001

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
                Down = False
                Up = False
                Right = False
                Left = False
                GameOver = True
            if ballY+10>=barY and ballX+7>barX and ballX-7<barX+170:
                Up = True
                Down = False
            if ballX<=window_x:
                Right = True
                Left = False
            if ballX>=window_x+window_width:
                Left = True
                Right = False
                          
        else: 
            gameWindow.fill((255,255,255))
            font = pygame.font.Font(None, 36)
            GOmsg = font.render(f'Ball Gir Gyi LOL !', True, (0,0,0))
            # score_text = font.render(f'Score: {Score*10}', True, (0,0,0))
            # HIscore = font.render(f'HI Score: {HI_Score*10}', True, (0,0,0))
            text = font.render(f'playAgain : ENTER', True, (0,0,0))
            # gameWindow.blit(score_text, (275, 315))
            # gameWindow.blit(HIscore, (275, 375))
            gameWindow.blit(GOmsg, (190, 215))
            gameWindow.blit(text, (180, 415)) 
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
                        ballX = 290
                        ballY = 290
                        Right = False
                        Left = False
                        Up = False
                        Down = False
                        velocity = 3.5
                        barX = 200
                        barY = window_height-30
                        barRight = False
                        barLeft = False
                        start = False
                        bricks = initializeBricks([40,20], 6)
            
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

pygame.quit()
exit()