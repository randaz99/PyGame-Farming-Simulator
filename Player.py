import pygame
from Entity import Entity

class Player(Entity):

    def __init__(self, img, pos=(100,100), color=None, colorKey=None):
        super().__init__(img=img, pos=pos, color=color, colorKey=colorKey)
        self.moveUp = False
        self.moveDown = False
        self.moveLeft = False
        self.moveRight = False
        self.speed = 5
        self.normalSpeed = 3
        self.boostedSpeed = 8
        self.speedBoostStartTime = pygame.time.get_ticks() - 3000


    def getInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moveUp = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moveDown = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moveRight = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moveLeft = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moveUp = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moveDown = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moveRight = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moveLeft = False


    def move(self, wallRects=[]):
        x = self.pos[0]
        y = self.pos[1]
        newX = x
        newY = y
        colliding = False

        if (self.moveUp == True):
            newY -= self.speed
        if (self.moveDown == True):
            newY += self.speed
        if (self.moveRight == True):
            newX += self.speed
        if (self.moveLeft == True):
            newX -= self.speed

        self.collisionRect = pygame.Rect(newX, newY, self.width, self.height)

        wallColideList = self.collisionRect.collidelistall(wallRects)

        if not wallColideList:
            self.pos = (newX, newY)
        else:
            self.pos = (x,y)
            self.collisionRect = pygame.Rect(x, y, self.width, self.height)

    def setSpeedBoost(self, active):
        if active:
            self.speed = self.boostedSpeed
            self.speedBoostStartTime = pygame.time.get_ticks()
        else:
            self.speed = self.normalSpeed

    def update(self):
        if pygame.time.get_ticks() - self.speedBoostStartTime > 3000:
            self.setSpeedBoost(False)