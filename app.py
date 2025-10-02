import streamlit as st
from openai import OpenAI
import os

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Math Exam Practice App")

# Instructions (like your GPT role)
SYSTEM_PROMPT = """
You are a practice-proctor and tutor. 
Ask one original precalculus question at a time. 
Use Socratic questions first; reveal solutions only after the student attempts an answer or asks for help.
"""

# Keep conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# User input
user_input = st.text_input("Enter your response:")

if st.button("Submit") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Show conversation history
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Tutor:** {msg['content']}")
