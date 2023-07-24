import pygame
from game.utils.constants import SCREEN_HEIGHT, SHIELD_TYPE


class BulletManager:
    def __init__(self):
        self.player_bullets = []
        self.enemy_bullets = []

    def update(self, game, screen):
        for bullet in self.enemy_bullets:
            bullet.update()
            if bullet.rect.y < 0:
                self.enemy_bullets.remove(bullet)
            for enemy in game.enemy_manager.enemies:
                if bullet.rect.colliderect(enemy.rect) and bullet.owner == "player":
                    game.enemy_manager.enemies.remove(enemy)
                    game.update.score()
                    self.player_bullets.remove(bullet)

        for bullet in self.enemy_bullets:
            bullet.update()
            if bullet.rect.y >= SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)

            if bullet.rect.colliderect(game.player.rect) and bullet.owner == "enemy":
                self.enemy_bullets.remove(bullet)
                if game.player.power_up_type != SHIELD_TYPE:
                    game.death_count += 1
                    game.playing = False
        for bullet in self.player_bullets:
            bullet.update()

            # Eliminar balas que salgan de la pantalla
            if bullet.rect.y < 0:
                self.player_bullets.remove(bullet)

            bullet.draw(screen)

    def draw(self, screen):
        for bullet in self.enemy_bullets:
            bullet.draw(screen)

        for bullet in self.player_bullets:
            bullet.draw(screen)

        # def shoot_enemy(self, bullet, enemy_manager):
        # for enemy in enemy_manager.enemies:
        # if bullet.rect.colliderect(enemy.rect) and bullet.owner == "player":
        # enemy_manager.enemies.remove(enemy)
        # self.player_bullets.remove(bullet)

    def add_bullet(self, bullet):
        if bullet.owner == "enemy" and len(self.enemy_bullets) < 1:
            self.enemy_bullets.append(bullet)
        elif bullet.owner == "player" and len(self.player_bullets) < 1:
            self.player_bullets.append(bullet)

    def check_enemy_collisions(self, game):
        for bullet in self.player_bullets:
            for enemy in game.enemy_manager.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.player_bullets.remove(bullet)
                    game.enemy_manager.enemies.remove(enemy)
                    game.enemy_killed()
                    break
