import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
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

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # spawn two asteroids
        for x in [a, b]:
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = x * 1.2
