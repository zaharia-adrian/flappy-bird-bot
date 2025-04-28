import pygame
import random
from random import  randrange

WIDTH = 1920
HEIGHT = 1080
FPS = 60
GAP = 125
GRAVITY = 9.8

class Ball:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = pygame.Color(randrange(0, 256),randrange(0, 256),randrange(0, 256))
        self.y_speed = 0.

        # 0 -> x_coef, 1 -> y_coef, 2-> y_speed_coef, 3-> bias
        self.coefs = [random.uniform(-100,100) for _ in range(4)]
        
    def update(self):
        if self.y_speed < GRAVITY:
            self.y_speed += GRAVITY / FPS * 6
        else:
            self.y_speed += GRAVITY / FPS    
        self.y_pos += self.y_speed
        
    def check_collision(self, wall, distance):
        if self.y_pos > HEIGHT + self.radius or self.y_pos + self.radius < 0:
            return True
        if abs(wall[1] - distance - self.x_pos) <= self.radius:
            if self.y_pos - wall[0] <= self.radius  or wall[0] + GAP - self.y_pos <= self.radius:
                return True
        return False
    
    def mutate(self):
        index = randrange(0,4)
        delta = random.uniform(-10,10)
        self.coefs[index]+=delta

    def check_flapp(self, wall, distance):
        x_dist = wall[1] - distance - self.x_pos
        y_dist = self.y_pos - wall[0] - GAP/2
        value = x_dist * self.coefs[0] + y_dist * self.coefs[1] + self.y_speed * self.coefs[2] + self.coefs[3]
        return (value > 0)

    def flapp(self):
        self.y_speed = -GRAVITY

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,(self.x_pos, self.y_pos), self.radius)
