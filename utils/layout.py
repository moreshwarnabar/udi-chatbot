import streamlit as st
from PIL import Image

def setup_ui():
    image_path = 'assets/ASU.png'
    col1, mid, col2 = st.columns([1, 1, 12])

    with col1:
        image = Image.open(image_path)
        st.image(image, width=100)

    with col2:
        st.title("University Design Institute")

    st.subheader("Chatbot")

def display_chat_history(messages):
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_input():
    return st.chat_input("Type your message here...")