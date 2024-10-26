import pygame
from Entity import Entity

class Mouse(Entity):

    def __init__(self, img=pygame.Surface((25, 25)), pos=(60, 60), color=None, colorKey=None, type='speed'):
        # Call the superclass constructor to initialize common attributes
        super().__init__(img=img, pos=pos, color=color, colorKey=colorKey)

        self.originalImg = img
        self.pressedWateringImg = self.originalImg.copy()
        self.pressedWateringImg.fill((50, 50, 255), special_flags=pygame.BLEND_RGB_MULT)
        self.pressedWateringImg.set_colorkey((50, 50, 255))
        self.wateringSoundEffect = pygame.mixer.Sound("data/sounds/watering-with-a-watering-can-39121_hYEqqE5m.mp3")
        self.playing = False

        self.mode = 0

        self.originalCleanseImg = pygame.image.load("data/images/pesticide.PNG")
        self.originalCleanseImg.set_colorkey((255, 255, 255))
        self.originalCleanseImg = pygame.transform.scale(self.originalCleanseImg,(self.originalImg.width, self.originalImg.width))
        self.originalCleanseImg = pygame.transform.flip(self.originalCleanseImg, True, False)
        self.pressedCleanseImg = self.originalCleanseImg.copy()
        self.pressedCleanseImg.fill((100, 222, 100), special_flags=pygame.BLEND_RGB_MULT)
        self.pressedCleanseImg.set_colorkey((100, 222, 100))

    def pressedWatering(self):
        self.img = self.pressedWateringImg
        if not self.playing:
            self.wateringSoundEffect.play(loops=-1)
            self.playing = True

    def unpressedWatering(self):
        self.img = self.originalImg
        self.wateringSoundEffect.stop()
        self.playing = False

    def move(self):
        cursorPos = pygame.mouse.get_pos()
        adjustedPos = (cursorPos[0], cursorPos[1] - 70)
        self.pos = adjustedPos
        self.collisionRect = pygame.Rect(adjustedPos[0], adjustedPos[1], self.width, self.height)

    def pressedCleanse(self):
        self.img = self.pressedCleanseImg

    def unpressedCleanse(self):
        self.img = self.originalCleanseImg

    def getInput(self, event):
        #print("getting input")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 :
                # print("Scroll wheel scrolled up")
                self.mode = (self.mode + 1) % 2
            elif event.button == 5:
                # print("Scroll wheel scrolled down")
                self.mode = (self.mode - 1) % 2

