import streamlit as st
import time
import random

WIDTH, HEIGHT = 10, 10

def run_game():
    snake = [(5, 5)]
    food = (random.randint(0, 9), random.randint(0, 9))
    score = 0

    grid_area = st.empty()
    score_area = st.empty()

    for _ in range(100):
        head_x, head_y = snake[0]

        fx, fy = food
        if fx > head_x:
            new_head = (head_x + 1, head_y)
        elif fx < head_x:
            new_head = (head_x - 1, head_y)
        elif fy > head_y:
            new_head = (head_x, head_y + 1)
        else:
            new_head = (head_x, head_y - 1)

        snake.insert(0, new_head)

        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake[1:]
        ):
            grid_area.text("💀 Game Over")
            break

        if new_head == food:
            score += 1
            food = (random.randint(0, 9), random.randint(0, 9))
        else:
            snake.pop()

        grid = [["⬛"] * WIDTH for _ in range(HEIGHT)]
        for x, y in snake:
            grid[y][x] = "🟩"
        fx, fy = food
        grid[fy][fx] = "🍎"

        grid_text = "\n".join("".join(row) for row in grid)

        grid_area.text(grid_text)
        score_area.write(f"Score: {score}")

        time.sleep(0.1)

st.title("🐍 AI Snake Game")

if st.button("Start Game"):
    run_game()