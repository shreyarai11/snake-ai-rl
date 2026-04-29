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

        # movement direction
        self.dx = BLOCK_SIZE
        self.dy = 0

        self.score = 0
        self.food = self._place_food()

    def _place_food(self):

        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)

        return (x, y)

    def play_step(self, action):

        # prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move snake
        self._move(action)

        head = self.snake[0]

        reward = 0
        game_over = False

        # collision check
        if self._is_collision(head):
            reward = -10
            game_over = True

            return reward, game_over, self.score

        # move body
        self.snake.insert(0, head)

        # food logic
        if head == self.food:

            self.score += 1
            reward = 10

            self.food = self._place_food()

        else:
            self.snake.pop()

        # draw everything
        self._update_ui()

        # game speed
        self.clock.tick(10)

        return reward, game_over, self.score

    def _is_collision(self, point):

        x, y = point

        # wall collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True

        # self collision
        if point in self.snake[1:]:
            return True

        return False

    def _update_ui(self):

        self.screen.fill((0, 0, 0))

        # snake
        for block in self.snake:

            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE)
            )

        # food
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE)
        )

        pygame.display.update()

    def _move(self, action):

        directions = [
            (BLOCK_SIZE, 0),     # RIGHT
            (0, BLOCK_SIZE),     # DOWN
            (-BLOCK_SIZE, 0),    # LEFT
            (0, -BLOCK_SIZE)     # UP
        ]

        idx = directions.index((self.dx, self.dy))

        # straight
        if action == [1, 0, 0]:
            new_dir = directions[idx]

        # right turn
        elif action == [0, 1, 0]:
            new_dir = directions[(idx + 1) % 4]

        # left turn
        else:
            new_dir = directions[(idx - 1) % 4]

        self.dx, self.dy = new_dir

        x, y = self.snake[0]

        new_head = (x + self.dx, y + self.dy)

        self.snake[0] = new_head