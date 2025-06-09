#!/usr/bin/env python3
"""
Snake Game using Pygame
Features:
- Snake movement with arrow keys
- Random food generation
- Collision detection (walls and self)
- Score display
- Game loop with frame rate control
"""

import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # Frames per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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


class Game:
    def __init__(self):
        """Initialize the game with screen, snake, and food"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)
        self.snake = Snake()
        self.food = Food()
        self.game_over = False

    def handle_events(self):
        """Process game events like quitting and key presses"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif self.game_over and event.key == pygame.K_RETURN:
                    self.reset_game()

    def update(self):
        """Update game state"""
        if not self.game_over:
            self.snake.handle_keys()
            
            # Update snake and check if game continues
            if not self.snake.update():
                self.game_over = True
                return
            
            # Check if snake eats food
            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.snake.score += 10
                self.food.randomize_position()
                
                # Make sure food doesn't appear on snake
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()

    def reset_game(self):
        """Reset the game to initial state"""
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False

    def render(self):
        """Render all game elements"""
        self.screen.fill(BLACK)
        
        # Draw grid lines
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))
        
        # Draw snake and food
        self.snake.render(self.screen)
        self.food.render(self.screen)
        
        # Display score
        score_text = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Display game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press Enter to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.update()

    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(SNAKE_SPEED)


if __name__ == "__main__":
    game = Game()
    game.run()
