import pygame
import torch
import numpy as np

from game.game import SnakeGameAI
from model import Linear_QNet

pygame.init()

# LOAD MODEL
model = Linear_QNet(11, 256, 3)

model.load_state_dict(
    torch.load("model.pth", map_location=torch.device("cpu"))
)

model.eval()

# CREATE GAME
game = SnakeGameAI()

BLOCK_SIZE = 20

# GET STATE
def get_state(game):

    head = game.snake[0]

    x = head[0]
    y = head[1]

    point_l = (x - BLOCK_SIZE, y)
    point_r = (x + BLOCK_SIZE, y)
    point_u = (x, y - BLOCK_SIZE)
    point_d = (x, y + BLOCK_SIZE)

    dir_l = game.dx == -BLOCK_SIZE
    dir_r = game.dx == BLOCK_SIZE
    dir_u = game.dy == -BLOCK_SIZE
    dir_d = game.dy == BLOCK_SIZE

    state = [

        # Danger straight
        (dir_r and game._is_collision(point_r)) or
        (dir_l and game._is_collision(point_l)) or
        (dir_u and game._is_collision(point_u)) or
        (dir_d and game._is_collision(point_d)),

        # Danger right
        (dir_u and game._is_collision(point_r)) or
        (dir_d and game._is_collision(point_l)) or
        (dir_l and game._is_collision(point_u)) or
        (dir_r and game._is_collision(point_d)),

        # Danger left
        (dir_d and game._is_collision(point_r)) or
        (dir_u and game._is_collision(point_l)) or
        (dir_r and game._is_collision(point_u)) or
        (dir_l and game._is_collision(point_d)),

        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,

        # Food location
        game.food[0] < x,
        game.food[0] > x,
        game.food[1] < y,
        game.food[1] > y
    ]

    return np.array(state, dtype=int)

# GAME LOOP
running = True

while running:

    state = get_state(game)

    state0 = torch.tensor(state, dtype=torch.float)

    prediction = model(state0)

    move = torch.argmax(prediction).item()

    final_move = [0, 0, 0]
    final_move[move] = 1

    reward, done, score = game.play_step(final_move)

    pygame.display.set_caption(f"Snake AI | Score: {score}")

    if done:
        print("Final Score:", score)
        running = False

pygame.quit()