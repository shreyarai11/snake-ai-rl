import streamlit as st

st.set_page_config(
    page_title="Snake AI",
    layout="centered"
)

st.title("🐍 Snake AI")

st.success("✅ Streamlit Deployment Successful!")

st.write("""
This project is a Snake AI built using:

- Python
- PyTorch
- Reinforcement Learning
- Pygame
- Streamlit

The AI was trained using Deep Q Learning.
""")

st.subheader("📈 Training Results")

st.write("""
The AI successfully learned:
- avoiding walls
- collecting food
- surviving longer
- maximizing score
""")

st.subheader("🎯 Final Performance")

st.write("""
Model trained successfully.

Local demo achieved high scores after training.
""")

st.info("Run demo.py locally to watch the AI play.")