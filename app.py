import streamlit as st
from utils.layout import setup_ui, display_chat_history, get_user_input
from services.response_generator import generate_response
from services.document_upload import process_document
from services.aws_client import get_s3_client, get_bedrock_agent_client
from frontend.sidebar import sidebar
from frontend.chat import chat
from utils.constants import REGION

s3_client = get_s3_client(REGION)
bedrock_agent_client = get_bedrock_agent_client(REGION)

# Set up UI components
setup_ui()

# File upload functionality
sidebar(s3_client, bedrock_agent_client)

# Accept user input and generate response
chat()