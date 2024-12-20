import random
import pygame
import sys
from Player import Player
from Wall import Wall
from Pickup import Pickup
from Plot import Plot
from Text import Text
from Mouse import Mouse

class Game:

    def __init__(self):
        pygame.init()

        # screen initialization
        scrRes = (1920, 1080)
        self.screen = pygame.display.set_mode(scrRes)
        pygame.display.set_caption('HW3_FarmingSim_Randazzo')
        self.clock = pygame.time.Clock()

        # background sound stuff
        pygame.mixer.init()
        pygame.mixer.music.load("data/sounds/mary-had-a-little-lamb-blues-instrumental-191224.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.backgroundNoise = pygame.mixer.Sound("data/sounds/ambience_farm_02wav-14806.mp3")
        self.backgroundNoise.set_volume(0.1)

        # title screen
        self.start = False
        self.title = Text(text="Farming Frenzy!", fontSize=100, pos=(self.screen.width // 2 - 300, self.screen.height // 2 - 150))
        self.titleText = Text(text="Press any key to start...", fontSize=50, pos=(self.screen.width // 2 - 200, self.screen.height // 2 - 50))
        self.screen.blit(self.title.img, self.title.collisionRect)
        self.screen.blit(self.titleText.img, self.titleText.collisionRect)
        pygame.display.update()
        while not self.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.start = True
                    self.backgroundNoise.play(loops=-1)

        # game object initializations
        self.stage = 0
        self.player = Player(img=pygame.image.load("data/images/player.png"), pos=(self.screen.width // 2 - 50,self.screen.height // 2 - 50), colorKey=(0,0,0))

        self.mouse = Mouse(img=pygame.image.load("data/images/WateringCan.PNG"), pos=(50,50), colorKey=(255,255,255))

        self.wallColor = (255,255,0)
        self.wall0 = Wall(img=pygame.Surface((1920, 20)), pos=(0,0), color=self.wallColor)
        self.wall1 = Wall(img=pygame.Surface((1920, 20)), pos=(0, 1060), color=self.wallColor)
        self.wall2 = Wall(img=pygame.Surface((20, 1080)), pos=(0, 0), color=self.wallColor)
        self.wall3 = Wall(img=pygame.Surface((20, 1080)), pos=(1900, 0), color=self.wallColor)
        #self.wallTest = Wall(pygame.image.load("data/player.png"), pos=(300,300))

        self.score = 0
        self.scoreText = Text(text=str(self.score), pos=(self.screen.width // 2 - 20,50))

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
            # draw everything
            self.draw()

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.player.getInput(event)
                self.mouse.getInput(event)

            # player movement
            self.player.move(self.wallRects)

            # mouse movement
            self.mouse.move()
            if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                match self.mouse.mode:
                    case 0:
                        self.mouse.pressedWatering()
                    case 1:
                        # print("in cleanse mode")
                        self.mouse.pressedCleanse()
            else:
                match self.mouse.mode:
                    case 0:
                        self.mouse.unpressedWatering()
                    case 1:
                        # print("in cleanse mode")
                        self.mouse.unpressedCleanse()

            # random spawns for boosts! (Pickups)
            if random.random() < 0.1 / 60:
                newPickup = Pickup(pos=(random.randrange(50, 1801), random.randrange(50, 1001)), type='speed')
                if random.random() < 0.5:
                    newPickup = Pickup(pos=(random.randrange(50, 1801), random.randrange(50, 1001)), type='water')
                self.pickups.append(newPickup)



            # Pickup detection
            for pickup in self.pickups:
                if self.player.collisionRect.colliderect(pickup.collisionRect):
                    pickup.playSound()
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
                match self.mouse.mode:
                    case 0:
                        if plot.collisionRect.colliderect(self.mouse.collisionRect) and pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                            plot.water()
                    case 1:
                        if plot.collisionRect.colliderect(self.mouse.collisionRect) and pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                            plot.cleanse()
                # random spawns for blight :(
                if random.random() < 0.01 / 60:
                    plot.blightCrop()
                plot.slowGrow()

            # print(self.score)
            self.scoreText.update(str(self.score))
            pygame.display.update()
            self.player.update()
            Plot.update()
            self.clock.tick(60)


    def draw(self):
        self.screen.fill((0, 0, 0))
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
                pygame.draw.rect(self.screen, pickup.highlightColor, pickup.highlightRect)
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