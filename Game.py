import random
import pygame
import sys
from Player import Player
from Wall import Wall
from Pickup import Pickup
from Entity import Entity
from Plot import Plot
from Text import Text

class Game:

    def __init__(self):
        pygame.init()

        scrRes = (1920, 1080)
        self.screen = pygame.display.set_mode(scrRes)
        pygame.display.set_caption('HW3_FarmingSim_Randazzo')
        self.clock = pygame.time.Clock()

        self.player = Player(img=pygame.image.load("data/player.png"), pos=(self.screen.width // 2 - 50,self.screen.height // 2 - 50), colorKey=(0,0,0))
        self.mouse = Entity(pygame.image.load("data/WateringCan.png"), pos=(50,50), colorKey=(255,255,255))

        self.wallColor = (255,255,0)
        self.wall0 = Wall(img=pygame.Surface((1920, 20)), pos=(0,0), color=self.wallColor)
        self.wall1 = Wall(img=pygame.Surface((1920, 20)), pos=(0, 1060), color=self.wallColor)
        self.wall2 = Wall(img=pygame.Surface((20, 1080)), pos=(0, 0), color=self.wallColor)
        self.wall3 = Wall(img=pygame.Surface((20, 1080)), pos=(1900, 0), color=self.wallColor)
        #self.wallTest = Wall(pygame.image.load("data/player.png"), pos=(300,300))

        self.score = 0
        self.scoreText = Text(text=str(self.score), pos=(self.screen.width // 2 - 20,50))

        self.speedColor = (255, 100, 0)
        self.waterColor = (60, 160, 255)
        #self.pickup1 = Pickup(pos=(99, 678), color=speedColor)

        # declaring entity lists
        self.playerThings = [self.player, self.mouse]
        self.pickups = []
        self.walls = [self.wall0, self.wall1, self.wall2, self.wall3]
        self.wallRects = []
        self.plots = []
        self.texts = [self.scoreText]

        # populating wallRects list
        for wall in self.walls:
            self.wallRects.append(wall.collisionRect)

        # populating plots list
        plotColor = (139, 69, 19)
        for i in range(80,1801,110):
                for j in range(50,1001,110):
                    if (j < 1001 / 2 - 50 or j > 1001 / 2 + 50) and (i <  1801/2 - 100 or i > 1801/2 + 100):
                        self.plots.append(Plot(pos=(i,j), color=plotColor))


    def run(self):
        pygame.mouse.set_visible(False)
        while True:
            self.screen.fill((0, 0, 0))

            # random spawns for boosts! (Pickups)
            if random.random() < 0.1/60:
                newPickup = Pickup(pos=(random.randrange(50, 1801), random.randrange(50, 1001)), color=self.speedColor)
                if random.random() < 0.5:
                    newPickup = Pickup(pos=(random.randrange(50,1801),random.randrange(50,1001)), color=self.waterColor, type='water')
                self.pickups.append(newPickup)

            # drawing all plots w/ their plants
            for plot in self.plots:
                if plot.color is not None:
                    pygame.draw.rect(self.screen, plot.color, plot.collisionRect)
                else:
                    self.screen.blit(plot.img, plot.pos)
                if plot.plant is not None and plot.plant.color is not None:
                    pygame.draw.rect(self.screen, plot.plant.color, plot.plant.collisionRect)
                elif plot.plant is not None:
                    self.screen.blit(plot.plant.img, plot.plant.pos)
            # drawing all walls
            for wall in self.walls:
                if wall.color is not None:
                    pygame.draw.rect(self.screen, wall.color, wall.collisionRect)
                else:
                    self.screen.blit(wall.img, wall.pos)
            # drawing all pickups
            for pickup in self.pickups:
                if pickup.color is not None:
                    pygame.draw.rect(self.screen, pickup.color, pickup.collisionRect)
                else:
                    self.screen.blit(pickup.img, pickup.pos)
            # drawing all player things
            for playerThing in self.playerThings:
                if playerThing.color is not None:
                    pygame.draw.rect(self.screen, playerThing.color, playerThing.collisionRect)
                else:
                    self.screen.blit(playerThing.img, playerThing.pos)
            # Drawing UI things
            for text in self.texts:
                self.screen.blit(text.img, text.collisionRect)


            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.player.getInput(event)

            # player movement
            self.player.move(self.wallRects)

            # mouse movement
            cursorPos = pygame.mouse.get_pos()
            adjustedPos = (cursorPos[0], cursorPos[1] - 70)
            self.mouse.pos = adjustedPos
            self.mouse.collisionRect = pygame.Rect(adjustedPos[0], adjustedPos[1], self.mouse.width, self.mouse.height)

            # Pickup detection
            for pickup in self.pickups:
                if self.player.collisionRect.colliderect(pickup.collisionRect):
                    self.pickups.remove(pickup)
                    match pickup.type:
                        case 'speed':
                            self.player.setSpeedBoost(True)
                        case 'water':
                            Plot.setWaterBoost(True)

            # Planting/growing detection
            for plot in self.plots:
                if self.player.collisionRect.colliderect(plot.collisionRect):
                    self.score += plot.interact()
                if plot.collisionRect.colliderect(self.mouse.collisionRect) and pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                    plot.water()
                plot.slowGrow()

            # print(self.score)
            self.scoreText.update(str(self.score))
            pygame.display.update()
            self.player.update()
            Plot.update()
            self.clock.tick(60)
