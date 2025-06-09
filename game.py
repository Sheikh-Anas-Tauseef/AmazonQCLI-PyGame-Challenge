"""
Game class for the Snake Game
Controls the main game loop, event handling, and overall game state
"""

import pygame
import sys

# Import game components
from snake import Snake
from food import Food

# Import constants from constants.py
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
    BLACK, WHITE, SNAKE_SPEED
)

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
