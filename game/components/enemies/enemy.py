import random
import pygame
from pygame.sprite import Sprite

from game.utils.constants import ENEMY_1, ENEMY_2, SCREEN_WIDTH


class Enemy(Sprite):
    ENEMY_WIDTH = 40
    ENEMY_HEIGHT = 60
    Y_POS = 20
    X_POS_LIST = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    SPEED_Y = 10
    SPEED_X = 5
    MOV_X = {0: "left", 1: "right"}

    def __init__(self):
        super().__init__()
        enemy_type = random.choice([1, 2])

        if enemy_type == 1:
            self.image = pygame.transform.scale(
                ENEMY_1, (self.ENEMY_WIDTH, self.ENEMY_HEIGHT)
            )
        else:
            self.image = pygame.transform.scale(
                ENEMY_2, (self.ENEMY_WIDTH, self.ENEMY_HEIGHT)
            )
        self.rect = self.image.get_rect()
        self.rect.x = random.choice(self.X_POS_LIST)
        self.rect.y = self.Y_POS
        self.speed_y = self.SPEED_Y
        self.speed_x = self.SPEED_X
        self.movement_x = self.MOV_X[random.randint(0, 1)]
        self.move_x_for = random.randint(30, 100)
        self.index = 0

    def update(self):
        self.rect.y += self.speed_y
        if self.movement_x == "left":
            self.rect.x -= self.speed_x
            if self.rect.x <= 0:
                self.movement_x = "right"
        else:
            self.rect.x += self.speed_x
            if self.rect.x >= SCREEN_WIDTH - self.ENEMY_WIDTH:
                self.movement_x = "left"
        self.change_movement_x()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def change_movement_x(self):
        self.index += 1
        print("Index: ", self.index)
        print("Mov_for: ", self.move_x_for)
        if self.index >= self.move_x_for:
            print(self.movement_x)
            if self.movement_x == "right":
                self.movement_x = "left"
            elif self.movement_x == "left":
                self.movement_x = "right"
            self.index = 0
