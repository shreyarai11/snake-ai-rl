import streamlit as st
import numpy as np
import time
import random

st.title("🐍 AI Snake Game (Visual)")

GRID_SIZE = 10

def create_grid(snake, food):
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    
    for s in snake:
        grid[s[0]][s[1]] = 1
    
    grid[food[0]][food[1]] = 2
    return grid

def move_snake(snake, direction):
    head = snake[0]

    if direction == 0:   # up
        new_head = [head[0]-1, head[1]]
    elif direction == 1: # right
        new_head = [head[0], head[1]+1]
    elif direction == 2: # down
        new_head = [head[0]+1, head[1]]
    else:                # left
        new_head = [head[0], head[1]-1]

    snake.insert(0, new_head)
    snake.pop()
    return snake

if st.button("▶ Run AI Snake"):

    snake = [[5, 5]]
    food = [random.randint(0, 9), random.randint(0, 9)]

    grid_placeholder = st.empty()

    score = 0

    for _ in range(50):

        direction = random.randint(0, 3)  # AI (random for now)

        snake = move_snake(snake, direction)

        head = snake[0]

        # collision check
        if (
            head[0] < 0 or head[0] >= GRID_SIZE or
            head[1] < 0 or head[1] >= GRID_SIZE
        ):
            break

        # food eat
        if head == food:
            score += 1
            snake.append(snake[-1])
            food = [random.randint(0, 9), random.randint(0, 9)]

        grid = create_grid(snake, food)

        grid_placeholder.dataframe(grid)

        time.sleep(0.2)

    st.success(f"Final Score: {score}")