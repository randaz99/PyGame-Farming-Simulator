import pygame

class Entity:
    def __init__(self, img=pygame.Surface((300,50)), pos=(50,50), color=None, colorKey=None):
        self.pos = pos
        self.img = img
        self.width = img.get_width()
        self.height = img.get_height()
        if color is None:
            self.img.set_colorkey(colorKey)
        self.color = color
        self.collisionRect = pygame.Rect(pos[0], pos[1], self.width, self.height)