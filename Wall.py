import pygame
from Entity import Entity

class Wall(Entity):

    def __init__(self, img=pygame.Surface((300, 50)), pos=(50, 50), color=None, colorKey=None):
        # Call the superclass constructor to initialize common attributes
        super().__init__(img=img, pos=pos, color=color, colorKey=colorKey)

