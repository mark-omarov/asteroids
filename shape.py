import pygame

class Shape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...] = ()

    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collides_with(self, other):
        # sub-classes must override
        return False