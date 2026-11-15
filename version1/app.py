import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

st.set_page_config(page_title="Mystery Library - Version 1", page_icon="🔐")
st.title("🔐 Mystery Library — Version 1")
st.write("Explore the library, find the clues and escape.")

SYSTEM_PROMPT = """
You are the Game Master of a fictional library escape room.
The room contains a desk, bookshelf, painting, locked drawer and exit door.
The desk parchment gives the order: Sun, Moon, Star, Crown.
The bookshelf gives Sun=4 and Moon=2.
The painting gives Star=1 and Crown=7.
The drawer combination is 4217. When opened, it contains the exit code 1935.
The exit opens with 1935.
Respond naturally to the player's actions, maintain the story, and do not
reveal solutions before the player investigates. This is Version 1: the
LLM manages the game conversation and is not protected by authoritative
Python game-state validation.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Room objects")
    st.write("🪑 Desk · 📚 Bookshelf · 🖼️ Painting")
    st.write("🗄️ Locked drawer · 🚪 Exit door")
    if st.button("Restart game"):
        st.session_state.messages = []
        st.rerun()

if not st.session_state.messages:
    st.info("You wake up in a locked library. Investigate the objects and find a way out.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("What would you like to do?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not API_KEY:
        answer = "Gemini API key not found. Copy .env.example to .env and add GEMINI_API_KEY."
    else:
        try:
            client = genai.Client(api_key=API_KEY)
            history = [
                types.Content(
                    role="user" if m["role"] == "user" else "model",
                    parts=[types.Part.from_text(text=m["content"])]
                )
                for m in st.session_state.messages
            ]
            response = client.models.generate_content(
                model=MODEL,
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=450
                )
            )
            answer = response.text or "The library remains quiet. Try another action."
        except Exception as exc:
            answer = f"Gemini API error: {exc}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
