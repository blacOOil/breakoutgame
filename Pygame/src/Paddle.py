import pygame
from src.constants import *
from src.Dependency import *

class Paddle:
    def __init__(self, skin=1):
        self.x = WIDTH/2 - 96
        self.y = HEIGHT - 96
        
        self.spacebar_pressed = False  # Track if spacebar is pressed
        self.magnetic_force = 50  # Control strength of the magnetic pull

        self.dx = 0

        self.size = 2

        self.width = self.size * 96  # 2 * 32 * 3 (scale)
        self.height = 48   # 16 * 3 (scale)

        self.SetImage(skin)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def SetImage(self, skin):
        self.skin = skin
        self.image = paddle_image_list[self.skin-1]

    def update(self, dt):
        key = pygame.key.get_pressed()

        # Handle paddle movement
        if key[pygame.K_LEFT]:
            self.dx = -PADDLE_SPEED
        elif key[pygame.K_RIGHT]:
            self.dx = PADDLE_SPEED
        else:
            self.dx = 0

        # Apply paddle movement within screen boundaries
        if self.dx < 0:
            self.rect.x = max(0, self.rect.x + self.dx * dt)
        else:
            self.rect.x = min(WIDTH - self.width, self.rect.x + self.dx * dt)

        # Check if spacebar is pressed for magnetic pull
        self.spacebar_pressed = key[pygame.K_SPACE]  # True when spacebar is held down

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
