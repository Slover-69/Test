import pygame
from constants import GREEN, WHITE, BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, UP, DOWN, LEFT, RIGHT, INITIAL_SNAKE_LENGTH

class Snake:
    def __init__(self):
        self.length = INITIAL_SNAKE_LENGTH
        # Initial position: center of the screen, moving right
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2) - i * BLOCK_SIZE) for i in range(self.length)]
        self.direction = DOWN # Start moving downwards
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Prevents the snake from immediately reversing on itself
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*BLOCK_SIZE)) % SCREEN_WIDTH), (cur[1] + (y*BLOCK_SIZE)) % SCREEN_HEIGHT)

        # Game over conditions
        # 1. Collision with boundaries (simple wrap-around for now, real collision later)
        # For a wrap-around effect:
        # if new[0] < 0: new = (SCREEN_WIDTH - BLOCK_SIZE, new[1])
        # elif new[0] >= SCREEN_WIDTH: new = (0, new[1])
        # if new[1] < 0: new = (new[0], SCREEN_HEIGHT - BLOCK_SIZE)
        # elif new[1] >= SCREEN_HEIGHT: new = (new[0], 0)

        # 2. Collision with self
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True # Collision occurred

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return False # No collision

    def grow(self):
        self.length += 1
        self.score +=1

    def check_collision_with_boundaries(self):
        head_x, head_y = self.get_head_position()
        if not (0 <= head_x < SCREEN_WIDTH and 0 <= head_y < SCREEN_HEIGHT):
            return True # Collision with boundary
        return False

    def check_collision_with_self(self):
        if self.get_head_position() in self.positions[1:]:
            return True # Collision with self
        return False

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1) # Border for each segment

    def reset(self):
        self.length = INITIAL_SNAKE_LENGTH
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2) - i * BLOCK_SIZE) for i in range(self.length)]
        self.direction = DOWN
        self.score = 0
