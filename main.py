import sys
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image = pygame.image.load("background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game Over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()

        screen.fill("black")
        screen.blit(bg_image, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
