import pygame
from Entity import Entity

class Pickup(Entity):

    def __init__(self, img=pygame.Surface((25, 25)), pos=(60, 60), color=None, colorKey=None, type='speed'):
        # Call the superclass constructor to initialize common attributes
        super().__init__(img=img, pos=pos, color=color, colorKey=colorKey)
        self.type = type
        self.useNoise = pygame.mixer.Sound("data/sounds/coin-collect-retro-8-bit-sound-effect-145251.mp3")
        self.useNoise.set_volume(0.5)
        self.highlightRect = pygame.Rect(pos[0]-1, pos[1]-1, self.width+2, self.height+2)
        self.highlightColor = (255,255,255)

        match type:
            case 'speed':
                self.color= (255, 100, 0)
            case 'water':
                self.color= (60, 160, 255)



    def playSound(self):
        self.useNoise.play()