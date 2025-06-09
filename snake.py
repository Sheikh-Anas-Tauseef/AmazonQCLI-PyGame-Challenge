"""
Snake class for the Snake Game
Handles snake movement, growth, and rendering
"""

import pygame

# Import constants from constants.py
from constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    GREEN, BLACK,
    UP, DOWN, LEFT, RIGHT
)

class Snake:
    def __init__(self):
        """Initialize the snake with starting position and direction"""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Start at center
        self.direction = RIGHT
        self.color = GREEN
        self.score = 0
        # Store the last direction to prevent 180-degree turns
        self.last_direction = self.direction

    def get_head_position(self):
        """Return the position of the snake's head"""
        return self.positions[0]

    def update(self):
        """Update the snake's position based on current direction"""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        
        # Game over if snake hits itself
        if (new_x, new_y) in self.positions[1:]:
            return False  # Game over
        
        # Update positions list
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
            
        # Update last direction
        self.last_direction = self.direction
        return True  # Game continues

    def reset(self):
        """Reset the snake to initial state"""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.last_direction = self.direction

    def render(self, surface):
        """Draw the snake on the game surface"""
        for position in self.positions:
            rect = pygame.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border

    def handle_keys(self):
        """Handle keyboard input for snake movement"""
        keys = pygame.key.get_pressed()
        
        # Prevent 180-degree turns (can't go directly opposite to current direction)
        if keys[pygame.K_UP] and self.last_direction != DOWN:
            self.direction = UP
        elif keys[pygame.K_DOWN] and self.last_direction != UP:
            self.direction = DOWN
        elif keys[pygame.K_LEFT] and self.last_direction != RIGHT:
            self.direction = LEFT
        elif keys[pygame.K_RIGHT] and self.last_direction != LEFT:
            self.direction = RIGHT
