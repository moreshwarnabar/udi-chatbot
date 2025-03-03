import streamlit as st
from utils.layout import setup_ui, display_chat_history, get_user_input
from services.response_generator import generate_response
from services.document_upload import process_document
from services.aws_client import get_s3_client, get_bedrock_agent_client
from utils.constants import REGION

s3_client = get_s3_client(REGION)
bedrock_agent_client = get_bedrock_agent_client(REGION)

# Set up UI components
setup_ui()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# File upload functionality
st.sidebar.title("Document Upload")
uploaded_file = st.sidebar.file_uploader("Upload a document (PDF, TXT, etc.)", type=["pdf", "txt", "docx"])

if uploaded_file:
    with st.spinner("Processing document..."):
        success = process_document(
            s3_client=s3_client, bedrock_client=bedrock_agent_client, uploaded_file=uploaded_file
        )
    if success:
        st.sidebar.success("Document uploaded and indexed successfully!")
    else:
        st.sidebar.error("Failed to upload or index the document.")

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