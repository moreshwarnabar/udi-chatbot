import streamlit as st
from utils.layout import setup_ui, display_chat_history, get_user_input
from services.response_generator import generate_response

# Set up UI components
setup_ui()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
display_chat_history(st.session_state.messages)

# Accept user input and generate response
if prompt := get_user_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="assets/user.jpeg"):
        st.markdown(prompt)

    with st.spinner(text="In progress..."):
        response = generate_response(st.session_state.messages, prompt)

    with st.chat_message("assistant", avatar="assets/asu-logo.jpeg"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})