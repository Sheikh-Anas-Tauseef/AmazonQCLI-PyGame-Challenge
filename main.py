#!/usr/bin/env python3
"""
Main entry point for the Snake Game
Initializes pygame and starts the game
"""

import pygame
from game import Game

def main():
    """Initialize pygame and start the game"""
    # Initialize pygame
    pygame.init()
    
    # Create and run the game
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
