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
    
    # AI agents will replace the dummy
    dummy_response = "I'm here for you. It's ok to feel this way, Would you like to talk more about it"
    st.session_state.chat_history.append({"role": "assistant", "content": dummy_response})

# Show response from the backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])