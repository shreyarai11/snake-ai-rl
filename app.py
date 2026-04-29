import streamlit as st
import pygame
import numpy as np
import time
import torch

from game.snake_game import SnakeGameAI
from ai.agent import Agent

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="Snake AI", layout="centered")

st.title("🐍 Snake AI using Deep Q-Learning")
st.write("AI is playing Snake in real time")

# -----------------------------
# LOAD MODEL
# -----------------------------
agent = Agent()

agent.model.load_state_dict(
    torch.load("model/model.pth", map_location=torch.device("cpu"))
)

agent.model.eval()

# -----------------------------
# CREATE GAME
# -----------------------------
game = SnakeGameAI(w=400, h=400)

# PLACEHOLDERS
score_placeholder = st.empty()
frame_placeholder = st.empty()

# -----------------------------
# GAME LOOP
# -----------------------------
while True:

    # GET CURRENT STATE
    state_old = agent.get_state(game)

    # GET ACTION
    final_move = agent.get_action(state_old)

    # PLAY STEP
    reward, done, score = game.play_step(final_move)

    # UPDATE SCORE
    score_placeholder.markdown(f"## 🎯 Score: {score}")

    # CONVERT SCREEN TO IMAGE
    frame = pygame.surfarray.array3d(game.display)

    # ROTATE IMAGE
    frame = np.rot90(frame)

    # FLIP IMAGE
    frame = np.flipud(frame)

    # SHOW IMAGE
    frame_placeholder.image(frame)

    # GAME OVER
    if done:
        st.success(f"Game Over! Final Score: {score}")
        break

    # SPEED CONTROL
    time.sleep(0.05)