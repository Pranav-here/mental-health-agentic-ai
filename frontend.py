# frontend.py
import os
import requests
import streamlit as st
from backend.config import BACKEND_URL

# Toggle your promo with an env var if you ever want to hide it
SHOW_PROMO = os.getenv("SHOW_PROMO", "1") == "1"

st.set_page_config(page_title="CalmCurrent", page_icon="🫧", layout="wide")
st.title("CalmCurrent")

# Safety copy, keeps it helpful and clear
with st.expander("Safety notice"):
    st.write(
        "This app does not diagnose, it only offers supportive conversation. "
        "If you are in immediate danger, call your local emergency number."
    )

# Sidebar promo kept small and quiet
if SHOW_PROMO:
    with st.sidebar:
        st.caption("Built by **Pranav Kuchibhotla**")
        st.markdown(
            "[Website](https://pranavkuchibhotla.com) • "
            "[LinkedIn](https://www.linkedin.com/in/pranavkuchibhotla/) • "
            "[GitHub](https://github.com/Pranav-here)"
        )
        st.caption("Open to AI, ML and Data Science internships")

# A short “About” section that also gives you credit
with st.expander("About this app"):
    st.write(
        "A student project focused on calm and practical mental health support, "
        "created by Pranav Kuchibhotla at Illinois Tech. "
        "Feedback is welcome."
    )

# Keep chat history in session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Chat input at the bottom
user_text = st.chat_input("Share what is on your mind")
if user_text:
    # Add user message
    st.session_state.chat.append({"role": "user", "content": user_text})

    # Call backend API, simple error handling
    try:
        r = requests.post(BACKEND_URL, json={"message": user_text}, timeout=20)
        r.raise_for_status()
        data = r.json()
        tool = data.get("tool_called", "None")
        reply = data.get("response", "Sorry, I could not generate a reply.")
        st.session_state.chat.append(
            # Tool note is light and keeps dev insight visible
            {"role": "assistant", "content": f"{reply}\n\n_(tool: {tool})_"}
        )
    except Exception as e:
        st.session_state.chat.append(
            {"role": "assistant", "content": f"Backend error, {e}"}
        )

# Render messages
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Soft footer, low contrast, center aligned
if SHOW_PROMO:
    st.markdown(
        """
        <div style="text-align:center; opacity:0.6; font-size:0.85rem; padding-top:1rem;">
            Made with care by <a href="https://pranavkuchibhotla.com" target="_blank">Pranav Kuchibhotla</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
