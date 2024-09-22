import pygame
from src.Dependency import *
from src.constants import *
from src.Dependency import *

class Brick:
    def __init__(self, x, y):
        self.tier = 0   # n -> 0
        self.color = 1  # 5 -> 1

        self.x = x
        self.y = y

        self.width = 96
        self.height = 48

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Movement properties
        self.speed = 100  # Speed of movement
        self.direction = -1  # 1 for right, -1 for left

    def Hit(self):
        gSounds['brick-hit2'].play()

        if self.tier > 0:
            if self.color == 1:
                self.tier -= 1
                self.color = 5
            else:
                self.color -= 1
        else:
            if self.color == 1:
                self.alive = False
            else:
                self.color -= 1

        if not self.alive:
            gSounds['brick-hit1'].play()

    def update(self, dt):
        if self.alive:
            # Move the brick horizontally
            self.rect.x += self.speed * self.direction
            
            # Check for boundaries
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.direction *= -1  # Reverse direction
                # Prevent the brick from moving out of bounds
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH

    def render(self, screen):
        if self.alive:
            screen.blit(brick_image_list[((self.color - 1) * 4) + self.tier], (self.rect.x, self.rect.y))
