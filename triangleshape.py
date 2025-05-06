import pygame
from shape import Shape
from constants import DEBUG_COLLISIONS, DEBUG_COLOR


def project_polygon(polygon, axis):
    dots = [vertex.dot(axis) for vertex in polygon]
    return min(dots), max(dots)


def polygon_collision(polygon1, polygon2):
    for i in range(len(polygon1)):
        edge = polygon1[(i + 1) % len(polygon1)] - polygon1[i]
        axis = pygame.Vector2(-edge.y, edge.x).normalize()

        min1, max1 = project_polygon(polygon1, axis)
        min2, max2 = project_polygon(polygon2, axis)

        if max1 < min2 or max2 < min1:
            return False

    for i in range(len(polygon2)):
        edge = polygon2[(i + 1) % len(polygon2)] - polygon2[i]
        axis = pygame.Vector2(-edge.y, edge.x).normalize()

        min1, max1 = project_polygon(polygon1, axis)
        min2, max2 = project_polygon(polygon2, axis)

        if max1 < min2 or max2 < min1:
            return False

    return True


class TriangleShape(Shape):
    def __init__(self, x, y, size, rotation=0):
        super().__init__(x, y)
        self.size = size
        self.radius = size
        self.rotation = rotation
        
    def get_vertices(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        line_width = 2
        pygame.draw.polygon(screen, "white", self.get_vertices(), line_width)
        
        if DEBUG_COLLISIONS:
            self.draw_debug(screen)
    
    def draw_debug(self, screen):
        pygame.draw.polygon(
            screen,
            DEBUG_COLOR,
            self.get_vertices(),
            1  # Line width
        )
            
        for point in self.get_vertices():
            pygame.draw.circle(
                screen,
                DEBUG_COLOR,
                point,
                2  # Radius
            )
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def collides_with(self, other):
        triangle = self.get_vertices()
        
        if isinstance(other, TriangleShape):
            return polygon_collision(triangle, other.get_vertices())
            
        elif hasattr(other, 'vertices'):
            asteroid_vertices = []
            for x, y in other.vertices:
                asteroid_vertices.append(pygame.Vector2(other.position.x + x, other.position.y + y))
            
            return polygon_collision(triangle, asteroid_vertices)
            
        elif hasattr(other, 'radius'):
            return self.triangle_circle_collision(triangle, other.position, other.radius)
            
        return False

    def triangle_circle_collision(self, triangle, circle_center, circle_radius):
        if self.point_in_triangle(circle_center, triangle):
            return True
        
        for i in range(len(triangle)):
            p1 = triangle[i]
            p2 = triangle[(i + 1) % len(triangle)]
            closest_point = self.closest_point_on_segment(circle_center, p1, p2)

            if (circle_center - closest_point).length() <= circle_radius:
                return True
        
        return False
    
    def point_in_triangle(self, p, triangle):
        p1, p2, p3 = triangle
        
        def area(p1, p2, p3):
            return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y)) / 2.0)
        
        A = area(p1, p2, p3)
        A1 = area(p, p2, p3)
        A2 = area(p1, p, p3)
        A3 = area(p1, p2, p)
        
        return abs(A - (A1 + A2 + A3)) < 0.1
    
    def closest_point_on_segment(self, p, a, b):
        ab = b - a
        ab_squared = ab.dot(ab)
        
        if ab_squared == 0:
            return a
        
        ap = p - a
        t = ap.dot(ab) / ab_squared
        t = max(0, min(1, t))
        
        return a + t * ab