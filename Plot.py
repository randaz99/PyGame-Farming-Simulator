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
        self.coolDownStartTime = pygame.time.get_ticks() - 500

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
                self.stageTimeRemaining = self.stageTime
        self.checkPlantStage()


    def interact(self):
        result = 0
        match self.plantStage:
            case -1:
                if pygame.time.get_ticks() - self.coolDownStartTime > 3000:
                    self.plantStage = 0
                    adjustedPlotPos = (self.pos[0] + 75 / 2, self.pos[1] + 75 / 2)
                    self.plant = Entity(img=pygame.Surface((25, 25)), pos=adjustedPlotPos, color=(0, 160, 0))
                    # print("Planted")
            case 2:
                self.resetPlot()
                result = 1
        return result


    def resetPlot(self):
        self.coolDownStartTime = pygame.time.get_ticks()
        self.plantStage = -1
        self.stageTimeRemaining = self.stageTime
        self.plant = None
        # print(self.coolDownStartTime)

    def slowGrow(self):
        self.water(speed=random.uniform(self.slowGrowSpeed-self.slowGrowSpeed, self.slowGrowSpeed+self.slowGrowSpeed), isSelf=True)

    def checkPlantStage(self):
        match self.plantStage:
            case 1:
                adjustedPlotPos = (self.pos[0] + 50 / 2, self.pos[1] + 50 / 2)
                self.plant = Entity(img=pygame.Surface((50, 50)), pos=adjustedPlotPos, color=(0, 160, 0))
            case 2:
                self.plant = Entity(img=pygame.Surface((100, 100)), pos=self.pos, color=(0, 160, 0))
