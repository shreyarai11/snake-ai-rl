imimport pygame
import torch
import random
import sys
from model import Linear_QNet

# INIT
pygame.init()

WIDTH, HEIGHT = 400, 400
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Snake Game")

font = pygame.font.SysFont("arial", 20)

# LOAD MODEL
model = Linear_QNet()
model.load_state_dict(torch.load("model.pth"))
model.eval()

# GAME VARIABLES
snake = [(200, 200)]
direction = (BLOCK, 0)
food = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))
score = 0

clock = pygame.time.Clock()

def get_state():
    head_x, head_y = snake[0]

    state = [
        head_x < BLOCK,
        head_x > WIDTH - BLOCK*2,
        head_y < BLOCK,
        head_y > HEIGHT - BLOCK*2,
        food[0] < head_x,
        food[0] > head_x,
        food[1] < head_y,
        food[1] > head_y,
        direction == (BLOCK, 0),
        direction == (-BLOCK, 0),
        direction == (0, BLOCK),
    ]

    return torch.tensor(state, dtype=torch.float)

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    state = get_state()
    prediction = model(state)
    move = torch.argmax(prediction).item()

    dx, dy = direction

    # MOVE LOGIC
    if move == 1:  # right turn
        direction = (dy, -dx)
    elif move == 2:  # left turn
        direction = (-dy, dx)

    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # COLLISION
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake
    ):
        print("Game Over! Final Score:", score)
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))
    else:
        snake.pop()

    # DRAW
    screen.fill((0, 0, 0))

    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*s, BLOCK, BLOCK))

    pygame.draw.rect(screen, (255, 0, 0), (*food, BLOCK, BLOCK))

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(10)