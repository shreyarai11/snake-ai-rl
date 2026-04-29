import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

class SnakeGameAI:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake AI")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.dx = BLOCK_SIZE
        self.dy = 0
        self.score = 0
        self.food = self._place_food()

    def _place_food(self):
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        return (x, y)

    def play_step(self, action):

        # 🟢 IMPORTANT: process events (prevents "Not Responding")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move
        self._move(action)
        head = self.snake[0]

        reward = 0
        game_over = False

        # collision
        if self._is_collision(head):
            reward = -10
            game_over = True
            return reward, game_over, self.score

        # move snake
        self.snake.insert(0, head)

        # food logic
        if head == self.food:
            self.score += 1
            reward = 10
            self.food = self._place_food()
        else:
            self.snake.pop()

        # 🟢 ALWAYS update UI (but slow speed keeps it smooth)
        self._update_ui()

        self.clock.tick(5)

        return reward, game_over, self.score

    def _is_collision(self, point):
        x, y = point

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True

        if point in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.screen.fill((0, 0, 0))

        for block in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()

    def _move(self, action):
        directions = [
            (BLOCK_SIZE, 0),
            (0, BLOCK_SIZE),
            (-BLOCK_SIZE, 0),
            (0, -BLOCK_SIZE)
        ]

        idx = directions.index((self.dx, self.dy))

        if action == [1, 0, 0]:
            new_dir = directions[idx]
        elif action == [0, 1, 0]:
            new_dir = directions[(idx + 1) % 4]
        else:
            new_dir = directions[(idx - 1) % 4]

        self.dx, self.dy = new_dir
        x, y = self.snake[0]
        self.snake[0] = (x + self.dx, y + self.dy)