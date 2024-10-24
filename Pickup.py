import pygame
from Entity import Entity

class Pickup(Entity):

    def __init__(self, img=pygame.Surface((25, 25)), pos=(60, 60), color=None, colorKey=None, type='speed'):
        # Call the superclass constructor to initialize common attributes
        super().__init__(img=img, pos=pos, color=color, colorKey=colorKey)
        self.type = type
        match type:
            case 'speed':
                self.color= (255, 100, 0)
            case 'water':
                self.color= (60, 160, 255)



