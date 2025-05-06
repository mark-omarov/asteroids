from shape import Shape

class CircleShape(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius: float = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius