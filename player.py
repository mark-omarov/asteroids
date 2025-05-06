import pygame
from constants import (
    PLAYER_BLINK_INTERVAL,
    PLAYER_RADIUS,
    PLAYER_SPAWN_TIME,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
)
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.spawn_timer = PLAYER_SPAWN_TIME
        self.blink_timer = 0
        self.visible = True
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 300
        self.max_speed = PLAYER_SPEED
        self.friction = 0.97

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.spawn_timer > 0:
            if not self.visible:
                return
        line_width = 2
        pygame.draw.polygon(screen, "white", self.triangle(), line_width)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.spawn_timer = max(self.spawn_timer - dt, 0)
        if self.spawn_timer > 0:
            self.blink_timer += dt
            if self.blink_timer >= PLAYER_BLINK_INTERVAL:
                self.visible = not self.visible
                self.blink_timer = 0

        self.shoot_timer -= dt

        keys = pygame.key.get_pressed()

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.apply_friction()

        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        self.position += self.velocity * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * self.acceleration * dt
        
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

    def apply_friction(self):
        self.velocity *= self.friction
        
        if self.velocity.length() < 0.1:
            self.velocity = pygame.Vector2(0, 0)

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = (
            pygame.math.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )