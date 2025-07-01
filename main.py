import pygame
import sys
import random

# --- Configuration ---
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)

# Directions
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont(None, 36)

    # Initial snake (list of positions), starting direction, and initial food
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = RIGHT
    food = place_food(snake)

    score = 0

    while True:
        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP    and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        # Move snake
        new_head = ((snake[0][0] + direction[0]) % GRID_WIDTH,
                    (snake[0][1] + direction[1]) % GRID_HEIGHT)

        # Check collisions
        if new_head in snake:
            game_over(screen, font, score)
            return

        snake.insert(0, new_head)

        # Check food
        if new_head == food:
            score += 1
            food = place_food(snake)
        else:
            snake.pop()

        # Draw everything
        screen.fill(BLACK)

        # Draw snake
        for pos in snake:
            rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

        # Draw food
        food_rect = pygame.Rect(food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

def place_food(snake):
    """Return a random position not occupied by the snake."""
    while True:
        pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if pos not in snake:
            return pos

def game_over(screen, font, score):
    """Display Game Over screen and wait for quit."""
    text1 = font.render("Game Over", True, RED)
    text2 = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//2 - 50))
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.flip()
    # Wait until user closes window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
