# Setup Streamlit
import streamlit as st

st.set_page_config(page_title="AI Therapist for Mental Health", layout='wide')
st.title("Placeholder name")

if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]

# User is able to ask a question


# Show response from the backend
