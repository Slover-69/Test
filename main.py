import pygame
import sys
import time # For countdown
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, RED, UP, DOWN, LEFT, RIGHT, SPEED, BLOCK_SIZE
from snake import Snake
from food import Food

def draw_text(surface, text, font, color, center_x, center_y):
    """Helper function to draw centered text."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (center_x, center_y)
    surface.blit(text_surface, text_rect)

def show_menu_screen(screen, font):
    """Displays the main menu and handles selection."""
    selected_option = 0 # 0 for Start, 1 for Quit
    options = ["Start Game", "Quit"]

    while True:
        screen.fill(BLACK)

        title_font = pygame.font.SysFont("monospace", 50)
        draw_text(screen, "PYTHON SNAKE", title_font, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        for i, option in enumerate(options):
            color = WHITE
            if i == selected_option:
                color = GREEN # Highlight selected option
            draw_text(screen, option, font, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN: # Enter key
                    return "start" if selected_option == 0 else "quit"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"

        clock.tick(SPEED) # Control menu refresh rate

def show_countdown(screen, font):
    """Displays a 5-second countdown on the screen."""
    for i in range(5, 0, -1):
        screen.fill(BLACK)
        countdown_text = font.render(str(i), True, WHITE)
        text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.flip()
        time.sleep(1) # Pause for 1 second

def game_loop():
    pygame.init()
    pygame.display.set_caption("Python Snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    global clock # Make clock global so menu can use it
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 35) # Font for score, game over, and menu

    # --- Menu Logic ---
    menu_choice = show_menu_screen(screen, font)
    if menu_choice == "quit":
        pygame.quit()
        sys.exit()

    # --- Countdown Logic ---
    if menu_choice == "start":
        show_countdown(screen, font)

    snake = Snake()
    food = Food()

    running = True
    game_over = False # This now primarily controls the game over *state*, not if the game loop is running
    game_active = True # This controls whether game logic (movement, collision) is processed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_active and not game_over: # Input for snake movement during active play
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
                elif game_over: # Input for game over screen
                    if event.key == pygame.K_ESCAPE:
                        running = False # Quit the game entirely
                    elif event.key == pygame.K_RETURN: # Press Enter to go back to menu
                        game_loop() # This will restart the whole game_loop, showing menu
                        return # Exit current game_loop instance
                    # Any other key for simple restart (if desired, but menu is better)
                    # else:
                    #     game_over = False
                    #     game_active = True
                    #     snake.reset()
                    #     food.generate()
                    #     while food.position in snake.positions:
                    #         food.generate()


        if game_active and not game_over:
            # Move snake
            collision_self = snake.move()

            if snake.check_collision_with_boundaries():
                game_over = True
                game_active = False # Stop game updates

            if collision_self:
                game_over = True
                game_active = False # Stop game updates

            if snake.get_head_position() == food.position:
                snake.grow()
                food.generate()
                while food.position in snake.positions:
                    food.generate()

            screen.fill(BLACK)
            snake.draw(screen)
            food.draw(screen)
            score_text = font.render(f"Score: {snake.score}", True, WHITE)
            screen.blit(score_text, (5, 5))

        elif game_over: # Game Over Screen
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER!", font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            draw_text(screen, f"Final Score: {snake.score}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text(screen, "Press ENTER for Menu", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
            draw_text(screen, "Press ESC to Quit", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + 40)
            # game_over_text = font.render("GAME OVER!", True, WHITE)
            # restart_text = font.render("Press ENTER for Menu (ESC to Quit)", True, WHITE)
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
