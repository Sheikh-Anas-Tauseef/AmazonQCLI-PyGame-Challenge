"""
Food class for the Snake Game
Manages food placement and rendering
"""

import pygame
import random

# Import constants from constants.py
from constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    RED, BLACK
)

class Food:
    def __init__(self):
        """Initialize food with random position"""
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        """Place food at a random position on the grid"""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

    def render(self, surface):
        """Draw the food on the game surface"""
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Border
