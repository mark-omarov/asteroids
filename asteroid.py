import pygame
import random
import math
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.vertices = self._generate_lumpy_vertices()
        
    def _generate_lumpy_vertices(self):
        num_vertices = random.randint(8, 12)  # Number of points to create a lumpy shape
        vertices = []
        
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            vertex_radius = self.radius * random.uniform(0.7, 1.1)
            x = math.cos(angle) * vertex_radius
            y = math.sin(angle) * vertex_radius
            vertices.append((x, y))
        return vertices

    def draw(self, screen):
        line_width = 2
        screen_vertices = []
        for x, y in self.vertices:
            screen_vertices.append((self.position.x + x, self.position.y + y))
        pygame.draw.polygon(
            screen,
            "white",
            screen_vertices,
            line_width
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius

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