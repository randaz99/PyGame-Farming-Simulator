import pygame
from Entity import Entity

class Text(Entity):

    def __init__(self,text="Default Text", fontSize=74, fontPath=None, pos=(50,50), color=(255,255,255)):
        self.font = pygame.font.Font(fontPath, fontSize)
        self.text = text
        self.img = self.font.render(text, True, color)
        # Call the superclass constructor to initialize common attributes
        super().__init__(img=self.img, pos=pos, color=color, colorKey=None)


    def update(self,text):
        self.img = self.font.render(text, True, self.color)
