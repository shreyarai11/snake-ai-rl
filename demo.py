import pygame
import torch
import numpy as np

from game.game import SnakeGameAI
from model import Linear_QNet

# -----------------------------
# INITIALIZE PYGAME
# -----------------------------
pygame.init()

# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------
model = Linear_QNet(11, 256, 3)

model.load_state_dict(
    torch.load("model.pth", map_location=torch.device("cpu"))
)

model.eval()

# -----------------------------
# CREATE GAME
# -----------------------------
game = SnakeGameAI()

# -----------------------------
# GET STATE FUNCTION
# -----------------------------
def get_state(game):

    head = game.snake[0]

    x = head[0]
    y = head[1]

    point_l = (x - 20, y)
    point_r = (x + 20, y)
    point_u = (x, y - 20)
    point_d = (x, y + 20)

    dir_l = game.direction == "LEFT"
    dir_r = game.direction == "RIGHT"
    dir_u = game.direction == "UP"
    dir_d = game.direction == "DOWN"

    state = [

        # Danger straight
        (dir_r and game.is_collision(point_r)) or
        (dir_l and game.is_collision(point_l)) or
        (dir_u and game.is_collision(point_u)) or
        (dir_d and game.is_collision(point_d)),

        # Danger right
        (dir_u and game.is_collision(point_r)) or
        (dir_d and game.is_collision(point_l)) or
        (dir_l and game.is_collision(point_u)) or
        (dir_r and game.is_collision(point_d)),

        # Danger left
        (dir_d and game.is_collision(point_r)) or
        (dir_u and game.is_collision(point_l)) or
        (dir_r and game.is_collision(point_u)) or
        (dir_l and game.is_collision(point_d)),

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

# -----------------------------
# GAME LOOP
# -----------------------------
running = True

while running:

    # CLOSE WINDOW
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # CURRENT STATE
    state = get_state(game)

    state0 = torch.tensor(state, dtype=torch.float)

    # MODEL PREDICTION
    prediction = model(state0)

    move = torch.argmax(prediction).item()

    # MOVE FORMAT
    final_move = [0, 0, 0]
    final_move[move] = 1

    # PLAY STEP
    reward, done, score = game.play_step(final_move)

    # WINDOW TITLE
    pygame.display.set_caption(f"Snake AI | Score: {score}")

    # GAME OVER
    if done:
        print("Final Score:", score)
        running = False

# -----------------------------
# QUIT
# -----------------------------
pygame.quit()