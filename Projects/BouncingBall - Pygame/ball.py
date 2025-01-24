import pygame
from os import system
from pygame.locals import *

# NOT SO REALISTIC PHYSICS COZ IT'S MADE IN 10 MINS ! KEYPRESSES ACCELERATE OR ENERGISE THE BALL< WHICH LOSES ENERGY OVER TIME !

pygame.init()
gameWindow = pygame.display.set_mode((600, 600))
pygame.display.set_caption("BouncingGola By AtharvaSrivastava")

system("cls")

window_rect = gameWindow.get_rect()
window_width = window_rect.width
window_height = window_rect.height
window_x = window_rect.x
window_y = window_rect.y

def main():
    exitGame = False
    clock = pygame.time.Clock()
    FPS = 120
    ballX = 290
    ballY = 290
    Right = False
    Left = False
    Up = False
    Down = False
    velocity = 7.0
    gravity = 3
    
    gameWindow.fill((255,255,255))
    pygame.event.pump()
    while not exitGame:
            event = None                            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True
                elif event.type == pygame.KEYDOWN:
                    velocity+=0.5
                    if (event.key == 1073741903):
                        Right = True
                        Left = False
                    if (event.key == 1073741904):
                        Left = True
                        Right = False
                    if (event.key == 1073741905):
                        Down = True
                        Up = False
                    if (event.key == 1073741906):
                        Up = True
                        Down = False
                    
            gameWindow.fill((255,255,255))
            pygame.draw.circle(gameWindow, (0,0,0), (ballX,ballY),10)
            if not(ballY>=window_y+window_height):
                ballY += gravity
                velocity-=0.01
            
            potential_energy = (1 - (ballY / window_height)) * 100
            potential_energy = max(0, min(potential_energy, 100)) 
            font = pygame.font.Font(None, 36)
            text = font.render(f"Potential Energy: {int(potential_energy)}", True, (0, 0, 0))
            gameWindow.blit(text, (10, 10))
            
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
                            
                            
                            
                            
            if ballY<=window_y:
                Down = True
                Up = False
            if ballY>=window_y+window_height:
                Up = True
                Down = False
            if ballX<=window_x:
                Right = True
                Left = False
            if ballX>=window_x+window_width:
                Left = True
                Right = False
                          
            
            
            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    main()

pygame.quit()
exit()