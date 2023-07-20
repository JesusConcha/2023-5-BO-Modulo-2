import pygame
from pygame.sprite import Sprite

from game.utils.constants import BULLET, BULLET_ENEMY


class Bullet(Sprite):
    BULLET_WIDTH = 10
    BULLET_HEIGTH = 20
    BULLET_PLAYER = pygame.transform.scale(BULLET, (BULLET_WIDTH, BULLET_HEIGTH))
    BULLET_ENEMY = pygame.transform.scale(BULLET, (BULLET_WIDTH, BULLET_HEIGTH))
    BULLETS = {"player": BULLET_PLAYER, "enemy": BULLET_ENEMY}
    SPEED = 20

    def __init__(self, spaceship):
        self.image = self.BULLETS[spaceship.type]
        self.rect = self.image.get_rect()
        self.rect.center = spaceship.rect.center
        self.owner = spaceship.type

    def update(self):
        self.rect.y += self.SPEED

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
