# Setup Streamlit
import streamlit as st

st.set_page_config(page_title="AI Therapist for Mental Health", layout='wide')
st.title("Placeholder name")

if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]

# User is able to ask a question
# Chat input
user_input = st.chat_input("What's up?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

# Show response from the backend
