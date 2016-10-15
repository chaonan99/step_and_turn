import pygame, sys
from pygame.locals import *

# Always call pygame.init() after import
pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((1024,768))
pygame.display.set_caption('Hello World!')
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480,380] = BLACK
print(DISPLAYSURF.get_locked())
del(pixObj)

catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'
'''
Main loop
1. Handles events.
2. Updates the game state.
3. Draws the game state to the screen.
'''
def main():
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            # Call pygame.quit() before sys.exit()
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)