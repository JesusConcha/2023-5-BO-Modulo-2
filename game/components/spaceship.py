import pygame
from pygame.sprite import Sprite
from game.components.bullets.bullet import Bullet
from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH


class Spaceship(Sprite):
    SPACESHIP_WIDTH = 40
    SPACESHIP_HEIGHT = 60
    SHIP_SPEED = 10
    X_POS = (SCREEN_WIDTH // 2) - SPACESHIP_WIDTH // 2
    Y_POS = 500

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            SPACESHIP, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.type = "player"
        self.max_height = SCREEN_HEIGHT // 2
        self.shooting_time = 0

    def shoot(self, bullet_manager):
        current_time = pygame.time.get_ticks()
        if self.shooting_time <= current_time:
            bullet = Bullet(self)
            bullet_manager.add_bullet(bullet)
            self.shooting_time = current_time + 500

    def update(self, user_input, game):
        if user_input[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= 10
            else:
                self.rect.x = SCREEN_WIDTH - self.rect.width

        elif user_input[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.x += 10
            else:
                self.rect.x = 0

        if user_input[pygame.K_UP] and self.rect.top > 0:
            if self.rect.y > self.max_height:
                self.rect.y -= 10

        elif user_input[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 10

        if self.rect.right <= 0:
            self.rect.x = SCREEN_WIDTH - 1
        elif self.rect.left >= SCREEN_WIDTH:
            self.rect.x = 1

        elif user_input[pygame.K_SPACE]:
            self.shoot(game)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def shoot(self, game):
        bullet = Bullet(self)
        game.bullet_manager.add_bullet(bullet)
