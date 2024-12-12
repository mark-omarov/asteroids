import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y, radius=SHOT_RADIUS):
        super().__init__(x, y, radius)

    def draw(self, screen):
        line_width = 2
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            line_width,
        )

    def update(self, dt):
        self.position += self.velocity * dt
