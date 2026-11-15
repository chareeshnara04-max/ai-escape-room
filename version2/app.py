import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from game_logic import new_game, handle_action

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
client = genai.Client(api_key=API_KEY) if API_KEY else None

st.set_page_config(page_title="Mystery Library - Version 2", page_icon="🔐", layout="wide")
st.title("🔐 Mystery Library — Version 2")
st.caption("Python validates game actions. Gemini is used only for optional storytelling.")

if "game" not in st.session_state:
    st.session_state.game = new_game()
if "messages" not in st.session_state:
    st.session_state.messages = []

state = st.session_state.game

def narrate(event):
    """Gemini may rephrase a validated event; fallback is the trusted Python event."""
    if client is None:
        return event
    prompt = (
        "You are a concise escape-room storyteller. Python has already validated "
        "the action. Rephrase this event without changing its outcome, adding clues, "
        "inventing objects, or revealing any information not in the event. Event: "
        + event
    )
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=180)
        )
        return response.text or event
    except Exception:
        return event

with st.sidebar:
    st.header("Game controls")
    if st.button("🔄 Restart game", use_container_width=True):
        st.session_state.game = new_game()
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.subheader("Room objects")
    st.write("🪑 Desk")
    st.write("📚 Bookshelf")
    st.write("🖼️ Painting")
    st.write("🗄️ Locked drawer")
    st.write("🚪 Exit door")
    st.divider()
    st.subheader("Inventory")
    if state["inventory"]:
        for item in state["inventory"]:
            st.write("• " + item)
    else:
        st.write("No items collected yet.")
    st.divider()
    st.subheader("Game progress")
    for label, key in [
        ("Desk", "desk_examined"),
        ("Bookshelf", "bookshelf_examined"),
        ("Painting", "painting_examined"),
        ("Drawer open", "drawer_open"),
        ("Escaped", "exit_open"),
    ]:
        st.write(f"{'✅' if state[key] else '⬜'} {label}")

st.subheader("Your adventure")
if not st.session_state.messages:
    st.info("You wake up in a locked library. Investigate the objects, collect clues and find the way out.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if state["exit_open"]:
    st.success("🎉 You escaped the Mystery Library!")
    st.balloons()
else:
    prompt = st.chat_input("What would you like to do?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        result = handle_action(state, prompt)
        # Only send already validated Python event to Gemini.
        answer = narrate(result["event"]) if result["ok"] and result["kind"] in {"clue", "drawer", "win"} else result["event"]
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
