import pygame
import random
import os
import threading

# This program creates a simple Snake game using the Pygame library. The snake moves around the screen, eats food, and grows in length while avoiding the borders. The game ends if the snake hits the borders.



class Spritee(pygame.sprite.Sprite): 
    def __init__(self, color, SizeOfSnake ,LengthOfSnakeList): 
        super().__init__() 
        self.Sx = LenOfSnakeList[0][0]
        self.Sy = LenOfSnakeList[0][1]
        self.image = pygame.Surface([SizeOfSnake,SizeOfSnake]) 
        self.image.fill(color)
        self.color = color
        self.image.set_colorkey(color)   
        for x,y in LenOfSnakeList:
            pygame.draw.rect(gameWindow, self.color, pygame.Rect(x,y,SizeOfSnake,SizeOfSnake)) 
            self.rect = self.image.get_rect() 
        
    @classmethod
    def Food (CLS,Fx,Fy):
        imageFood = pygame.Surface([12,12])
        pygame.draw.rect(gameWindow, (255,0,0), pygame.Rect(Fx,Fy,12,12)) 
        CLS.Food_rect = imageFood.get_rect() 
        






root = pygame.init()
gameWindow = pygame.display.set_mode((650,650))
pygame.display.set_caption("Saampon Ke Sath Khilwaad")



WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)



pygame.mixer.init()

pygame.mixer.music.load('start.mp3')
pygame.mixer.music.play()


exitGame = False
gameOver = False
xVelocity = 2
yVelocity = 2
Score = 0
SizeOfSnake = 12
LenOfSnake = 1
LenOfSnakeList = []
Right = False
Left = False
Up = False
Down = False
Sx = 313
Sy = 313
Fx = random.randint(25,625)
Fy = random.randint(25,625)
clock = pygame.time.Clock()
FPS = 90
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
        if (Score>HI_Score):
            HI_Score=Score
            with open('hiscore.txt' , 'w') as f:
                f.write(str(HI_Score))
        
        gameWindow.fill(WHITE)
        font = pygame.font.Font(None, 36)
        GOmsg = font.render(f'Saamp Mar Gaya LOL !', True, (0,0,0))
        score_text = font.render(f'Score: {Score*10}', True, (0,0,0))
        HIscore = font.render(f'HI Score: {HI_Score*10}', True, (0,0,0))
        text = font.render(f'PlayAgain : ENTER', True, (0,0,0))
        gameWindow.blit(score_text, (275, 315))
        gameWindow.blit(HIscore, (275, 375))
        gameWindow.blit(GOmsg, (275, 215))
        gameWindow.blit(text, (275, 415))
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if(event.key == 13):
                    pygame.mixer.music.load('start.mp3')
                    pygame.mixer.music.play()
                    exitGame = False
                    gameOver = False
                    xVelocity = 3
                    yVelocity = 3
                    Score = 0
                    SizeOfSnake = 12
                    LenOfSnake = 1
                    LenOfSnakeList = []
                    Right = False
                    Left = False
                    Up = False
                    Down = False
                    Sx = 313
                    Sy = 313
                    Fx = random.randint(25,625)
                    Fy = random.randint(25,625)
                    clock = pygame.time.Clock()
                    FPS = 60
            if (event.type == pygame.QUIT):
                exitGame = True
                
    else:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exitGame = True
                
            elif (event.type == pygame.KEYDOWN):
                if (event.key == 1073741903):
                    Right = True
                    Left,Up,Down = False,False,False
                if (event.key == 1073741904):
                    Left = True
                    Right,Up,Down = False,False,False
                if (event.key == 1073741905):
                    Down = True
                    Left,Up,Right = False,False,False
                if (event.key == 1073741906):
                    Up = True
                    Left,Right,Down = False,False,False
                                
        if Right:
                Sx+=xVelocity
        elif Left:
                Sx-=xVelocity
        elif Up:
                Sy-=yVelocity
        elif Down:
                Sy+=yVelocity
            
        if ((abs(Sx - Fx) < 15) and (abs(Sy - Fy) < 15)):
            pygame.mixer.music.load('eat.mp3')
            pygame.mixer.music.play()
            Fx = random.randint(25,625)
            Fy = random.randint(25,625)
            xVelocity+=0.2
            yVelocity+=0.2
            Score+=1
            LenOfSnake+=5
            
            
        if (Sx<0):
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play()
            gameOver = True
        elif (Sx>650-SizeOfSnake):
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play()
            gameOver = True
        elif (Sy<0):
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play()
            gameOver = True
        elif (Sy>650-SizeOfSnake):
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play()
            gameOver = True
            
            
        head = []
        head.append(Sx)
        head.append(Sy)
        LenOfSnakeList.append(head)
        
        if (len(LenOfSnakeList)>LenOfSnake):
            del LenOfSnakeList[0]
            
        if (head in LenOfSnakeList[:-1]):
            gameOver = True
            pygame.mixer.music.load('GameOver.mp3')
            pygame.mixer.music.play()

        
            
        gameWindow.fill(WHITE)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {Score*10}', True, (0,0,0))
        gameWindow.blit(score_text, (10, 10))
        HIscore = font.render(f'HI Score: {HI_Score*10}', True, (0,0,0))
        gameWindow.blit(HIscore, (10, 35))
        snake = Spritee(BLACK,SizeOfSnake,LenOfSnakeList)
        food = Spritee.Food(Fx,Fy)
        pygame.display.update()
        clock.tick(FPS)
    pygame.display.update()
    clock.tick(FPS)
    



pygame.quit()
exit()