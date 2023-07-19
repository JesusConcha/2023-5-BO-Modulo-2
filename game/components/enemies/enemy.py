import random
import pygame
from pygame.sprite import Sprite

from game.utils.constants import ENEMY_1, SCREEN_WIDTH


class Enemy(Sprite):
    ENEMY_WIDTH = 40
    ENEMY_HEIGHT = 60
    Y_POS = 20
    X_POS_LIST = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    SPEED_Y = 10
    SPEED_X = 5
    MOV_X = {0: "left", 1: "rigth"}

    def __init__(self):
        self.image = pygame.transform.scale(
            ENEMY_1, (self.ENEMY_WIDTH, self.ENEMY_HEIGHT)
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS_LIST[random.randint(0, 10)]
        self.rect.y = self.Y_POS
        self.speed_y = self.speed_y
        self.speed_x = self.speed_x
        self.movement_x = self.MOV_X[random.randint(0, 1)]
        self.move_x_for = random.randint(30, 100)
        self.index = 0

    def update(self):
        self.rect.y += self.speed_y
        if self.movement_x == "left":
            self.rect.x -= self.speed_x
        else:
            self.rect.x += self.speed_x
        self.change_movement_x()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def change_movement_x(self):
        self.index += 1
        print("Index: ", self.index)
        print("Mov_for: ", self.move_x_for)
        if self.index >= self.move_x_for:
            print(self.movement_x)
            if self.movement_x == "rigth":
                self.movement_x == "left"
            elif self.movement_x == "left":
                self.movement_x == "rigth"
            self.index = 0
