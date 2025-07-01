# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255) # Added for potential score display or other UI elements

# Game specific
BLOCK_SIZE = 20
SPEED = 10 # Frames per second (Reduced from 15 for slower snake)
INITIAL_SNAKE_LENGTH = 3

# Directions (using tuples for coordinates is common in Pygame)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
