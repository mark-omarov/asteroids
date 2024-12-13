import pygame
from constants import PLAYER_SPAWN_TIME


class GameManager(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...] = ()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, *self.containers)
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.respawn_timer = 0.0  # seconds

    def update(self, dt):
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
        else:
            self.respawn_timer = 0

    def add_score(self, amount):
        self.score += amount

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.respawn_timer = PLAYER_SPAWN_TIME

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.game_over = False
