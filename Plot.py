import random

import pygame
from Entity import Entity

class Plot(Entity):
    wateringSpeed = 1.0
    boost = 10.0
    waterBoostStartTime = pygame.time.get_ticks() - 3000
    slowGrowSpeed = 0.05
    stageTime = 2*60

    def __init__(self, img=pygame.Surface((100, 100)), pos=(50, 50), color=None, colorKey=None):
        # Call the superclass constructor to initialize common attributes
        super().__init__(img=img, pos=pos, color=color, colorKey=colorKey)
        self.plantStage = -1
        self.stageTimeRemaining = self.stageTime
        self.plant = None
        self.coolingDown = False
        self.coolDownStartTime = -3000
        self.plantingSoundEffect = pygame.mixer.Sound("data/Sounds/Record 2024-10-24 at 18h18m13s-[AudioTrimmer.com].wav")
        self.harvestingSoundEffect = pygame.mixer.Sound("data/Sounds/hand-digging-dirt-leaves-crunch-32630-[AudioTrimmer.com].mp3")
        self.plantingSoundEffect.set_volume(0.5)
        self.harvestingSoundEffect.set_volume(0.5)
        self.isBlight = False
        self.healthyColor = (0, 160, 0)
        self.blightColor = (160, 160, 80)

    @classmethod
    def setWaterBoost(cls, active):
        if active:
            cls.boost = 10
            cls.waterBoostStartTime = pygame.time.get_ticks()
        else:
            cls.boost = 1

    @classmethod
    def update(cls):
        if pygame.time.get_ticks() - cls.waterBoostStartTime > 4000:
            cls.setWaterBoost(False)

    def water(self, speed=wateringSpeed, isSelf=False):
        # print(self.plantStage)
        if self.plantStage > -1 and self.plantStage < 2:
            # print(self.stageTimeRemaining)
            if isSelf:
                self.stageTimeRemaining -= speed
            else:
                self.stageTimeRemaining -= speed * self.boost
            if self.stageTimeRemaining < 0:
                self.plantStage += 1
                self.stageTimeRemaining = self.stageTime - 1
        elif self.plantStage == 2:
            # print(self.stageTimeRemaining)
            if isSelf:
                self.stageTimeRemaining -= speed
            else:
                self.stageTimeRemaining -= speed * self.boost
        self.checkPlantStage()


    def interact(self):
        result = 0
        match self.plantStage:
            case -1:
                if pygame.time.get_ticks() - self.coolDownStartTime > 3000:
                    self.plantStage = 0
                    adjustedPlotPos = (self.pos[0] + 75 / 2, self.pos[1] + 75 / 2)
                    color = self.healthyColor
                    if self.isBlight:
                        color = self.blightColor
                    self.plant = Entity(img=pygame.Surface((25, 25)), pos=adjustedPlotPos, color=color)
                    # print("Planted")
                    self.plantingSoundEffect.play()
            case 2:
                self.resetPlot()
                result = 1
                self.harvestingSoundEffect.play()
        return result


    def resetPlot(self):
        self.coolDownStartTime = pygame.time.get_ticks()
        self.plantStage = -1
        self.stageTimeRemaining = self.stageTime
        self.plant = None
        self.isBlight = False
        # print(self.coolDownStartTime)

    def slowGrow(self):
        if not self.isBlight:
            self.water(speed=random.uniform(self.slowGrowSpeed-self.slowGrowSpeed, self.slowGrowSpeed+self.slowGrowSpeed), isSelf=True)
        else:
            self.water(speed=random.uniform(-5*(self.slowGrowSpeed-self.slowGrowSpeed), -5*(self.slowGrowSpeed+self.slowGrowSpeed)), isSelf=True)
            print(f"Stage: {self.plantStage}")
            print(self.stageTimeRemaining)
            if self.stageTimeRemaining > self.stageTime:
                self.plantStage -= 1
                self.stageTimeRemaining = 0
                print("shrinking")
                if self.plantStage < 0:
                    self.resetPlot()
                    print("dying")


    def checkPlantStage(self):
        color = self.healthyColor
        if self.isBlight:
            color = self.blightColor
        match self.plantStage:
            case 0:
                adjustedPlotPos = (self.pos[0] + 75 / 2, self.pos[1] + 75 / 2)
                self.plant = Entity(img=pygame.Surface((25, 25)), pos=adjustedPlotPos, color=color)
            case 1:
                adjustedPlotPos = (self.pos[0] + 50 / 2, self.pos[1] + 50 / 2)
                self.plant = Entity(img=pygame.Surface((50, 50)), pos=adjustedPlotPos, color=color)
            case 2:
                self.plant = Entity(img=pygame.Surface((100, 100)), pos=self.pos, color=color)

    def blightCrop(self):
        if self.plantStage > -1:
            self.plant.color = self.blightColor
            self.isBlight = True
            print("BLIGHT!")
