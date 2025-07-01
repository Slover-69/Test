import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, UP, DOWN, LEFT, RIGHT, SPEED, BLOCK_SIZE
from snake import Snake
from food import Food

def game_loop():
    pygame.init()
    pygame.display.set_caption("Python Snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 35) # Font for score and game over

    snake = Snake()
    food = Food()

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_over: # Only allow direction change if game is not over
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
                else: # If game is over, any key press restarts the game
                    if event.key == pygame.K_ESCAPE: # Specific key to quit after game over
                        running = False
                    else:
                        game_over = False
                        snake.reset()
                        food.generate()
                        # Ensure new food is not generated on the snake
                        while food.position in snake.positions:
                            food.generate()


        if not game_over:
            # Move snake
            collision_self = snake.move() # move() now returns True if collision with self occurs

            # Check for collision with boundaries
            if snake.check_collision_with_boundaries():
                game_over = True

            # Check for collision with self (returned by move)
            if collision_self: # check_collision_with_self is now implicitly handled by move()
                game_over = True

            # Check if snake eats food
            if snake.get_head_position() == food.position:
                snake.grow()
                food.generate()
                # Ensure new food is not generated on the snake
                while food.position in snake.positions:
                    food.generate()

            # Drawing
            screen.fill(BLACK)
            snake.draw(screen)
            food.draw(screen)

            # Display Score
            score_text = font.render(f"Score: {snake.score}", True, WHITE)
            screen.blit(score_text, (5, 5))

        else: # Game Over Screen
            screen.fill(BLACK)
            game_over_text = font.render("GAME OVER!", True, WHITE)
            restart_text = font.render("Press any key to Restart (ESC to Quit)", True, WHITE)
            final_score_text = font.render(f"Final Score: {snake.score}", True, WHITE)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3 - game_over_text.get_height() // 2))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - final_score_text.get_height() // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT * 2 // 3 - restart_text.get_height() // 2))


        pygame.display.flip() # Update the full display
        clock.tick(SPEED)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    game_loop()
