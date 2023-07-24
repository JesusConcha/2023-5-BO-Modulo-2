import pygame
from game.components.bullets.bullet_manager import BulletManager
from game.components.enemies.enemy_manager import EnemyManager
from game.components.menu import Menu
from game.components.power_ups.power_up_manager import PowerUpManager
from game.utils.constants import (
    BG,
    FONT_STYLE,
    ICON,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    FPS,
    DEFAULT_TYPE,
)
from game.components.spaceship import Spaceship
from sys import exit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.is_game_over = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.running = False
        self.menu = Menu("Press any key to start...", self.screen)
        self.death_count = 0
        self.score = 0
        self.highest_score = 0
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.is_game_over = False
        self.score = 0
        self.enemy_manager.reset()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                exit()

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self, self.screen)
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.draw_score()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()

    def player_hit(self):
        self.is_game_over = (
            True  # Establecer el estado de Game Over al morir el jugador
        )
        self.death_count += 1
        print(f"Total deaths: {self.death_count}")

    def enemy_killed(self):
        self.score += 1

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed

    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.menu.draw(self.screen)
        else:
            self.update_highest_score()
            self.menu.update_message(self.screen, "Game Over, Press any key to restart")
            self.menu.update_message(self.screen, f"Your score: {self.score}", 30)
            self.menu.update_message(
                self.screen, f"Highest score: {self.highest_score}", 60
            )
            self.menu.update_message(
                self.screen, f"Total deaths: {self.death_count}", 90
            )

        icon = pygame.transform.scale(ICON, (80, 120))
        self.screen.blit(icon, (half_screen_width - 50, half_screen_height - 150))

        self.menu.update(self)

    def update_score(self):
        self.score += 1

    def update_highest_score(self):
        if self.score > self.highest_score:
            self.highest_score = self.score

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round(
                (self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2
            )
            if time_to_show > 0:
                message = f"{self.player.power_up_type.capitalize()} is enable for {time_to_show} second"
                self.menu.update_message(self.screen, message, -500, (255, 255, 255))
            else:
                self.player.has_power_up = False
                self.player.power_up_type = DEFAULT_TYPE
                self.player.set_image()

    def draw_total_deaths(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f"Total deaths: {self.death_count}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1000, 100)
        self.screen.blit(text, text_rect)

    def add_bullet(self, bullet):
        if bullet.owner == "enemy" and len(self.bullet_manager.enemy_bullets) < 1:
            self.bullet_manager.enemy_bullets.append(bullet)
        elif bullet.owner == "player" and len(self.bullet_manager.player_bullets) < 1:
            self.bullet_manager.player_bullets.append(bullet)
