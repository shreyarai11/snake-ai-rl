import streamlit as st
import random

st.title("🐍 AI Snake Game (Simulation)")

st.write("This is a simplified AI simulation of a trained Snake agent.")

if st.button("Run AI"):
    score = 0
    
    for _ in range(50):
        ai_move = random.randint(0, 2)
        correct_move = random.randint(0, 2)
        
        if ai_move == correct_move:
            score += 1

    st.success(f"Final Score: {score}")