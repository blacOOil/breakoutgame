import pygame
from src.Dependency import *
from src.constants import *
from src.Dependency import *

class Brick:
    def __init__(self, x, y):
        self.tier = 0  # Tier 0 is the weakest, can increase for stronger bricks
        self.color = 1  # Color index for brick; 1 is the weakest color, 5 is the strongest

        self.x = x
        self.y = y

        self.width = 96
        self.height = 48

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Movement properties
        self.speed = 100  # Speed of movement
        self.direction = -1  # 1 for right, -1 for left (moving left initially)

    def Hit(self):
        """Called when the brick is hit by the ball."""
        if self.alive:
            gSounds['brick-hit2'].play()

            # Decrease tier and color on hit
            if self.tier > 0:
                if self.color == 1:
                    self.tier -= 1  # Decrease tier
                    self.color = 5  # Reset to the strongest color
                else:
                    self.color -= 1  # Decrease color
            else:
                if self.color == 1:
                    self.alive = False  # Destroy the brick if it's at the lowest color and tier
                else:
                    self.color -= 1  # Decrease color

            # Play the destruction sound if the brick is destroyed
            if not self.alive:
                gSounds['brick-hit1'].play()

    def update(self, dt):
        """Updates the brick's position and handles movement logic."""
        if self.alive:
            # Move the brick horizontally with frame-rate independent speed
            self.rect.x += self.speed * self.direction * dt

            # Check for boundaries
            if self.rect.left < 0 or self.rect.right > WIDTH:
                # Reverse direction if the brick hits the screen's edges
                self.direction *= -1

                # Keep the brick within bounds
                if self.rect.left < 0:
                    self.rect.left = 0
                elif self.rect.right > WIDTH:
                    self.rect.right = WIDTH

    def render(self, screen):
        """Renders the brick onto the screen if it is still alive."""
        if self.alive:
            # Fetch the correct image based on the brick's color and tier
            screen.blit(brick_image_list[((self.color - 1) * 4) + self.tier], (self.rect.x, self.rect.y))
