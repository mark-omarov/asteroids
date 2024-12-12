import sys
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SHOT_HIT_SCORE,
)
from gamemanager import GameManager
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image = pygame.image.load("background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    GameManager.containers = updatable

    game_manager = GameManager()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        if player.spawn_timer <= 0:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_manager.lose_life()
                    if game_manager.game_over:
                        print("Game Over!")
                        sys.exit()
                    player.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    break

                for shot in shots:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        game_manager.add_score(SHOT_HIT_SCORE)

        screen.fill("black")
        screen.blit(bg_image, (0, 0))

        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"Score: {game_manager.score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {game_manager.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()

        # limit 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
