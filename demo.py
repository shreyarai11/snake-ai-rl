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
game = SnakeGameAI(w=400, h=400)

# -----------------------------
# GET STATE FUNCTION
# -----------------------------
def get_state(game):

    head = game.snake[0]

    point_l = pygame.Vector2(head.x - 20, head.y)
    point_r = pygame.Vector2(head.x + 20, head.y)
    point_u = pygame.Vector2(head.x, head.y - 20)
    point_d = pygame.Vector2(head.x, head.y + 20)

    dir_l = game.direction == pygame.K_LEFT
    dir_r = game.direction == pygame.K_RIGHT
    dir_u = game.direction == pygame.K_UP
    dir_d = game.direction == pygame.K_DOWN

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
        game.food.x < game.head.x,
        game.food.x > game.head.x,
        game.food.y < game.head.y,
        game.food.y > game.head.y
    ]

    return np.array(state, dtype=int)

# -----------------------------
# GAME LOOP
# -----------------------------
running = True

while running:

    # CLOSE WINDOW EVENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # GET CURRENT STATE
    state = get_state(game)

    state0 = torch.tensor(state, dtype=torch.float)

    # PREDICT MOVE
    prediction = model(state0)

    move = torch.argmax(prediction).item()

    # CONVERT TO MOVE FORMAT
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
# QUIT GAME
# -----------------------------
pygame.quit()