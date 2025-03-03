# UDI Chatbot

## Overview

UDI Chatbot is a Streamlit-based application designed to facilitate interactive conversations while leveraging AWS Bedrock for response generation. The chatbot supports document uploads, allowing users to index and retrieve knowledge from uploaded files.

## Features

- Streamlit UI for an intuitive chat experience
- File upload functionality for document-based knowledge retrieval
- AWS Bedrock integration for AI-generated responses
- Chat history management
- S3 storage for document uploads
- Automated knowledge base synchronization

## Installation

### Prerequisites

- Python 3.8+
- AWS credentials configured for Bedrock and S3 access
- Required dependencies (see `requirements.txt`)

### Setup

```sh
git clone <repo-url>
cd moreshwarnabar-udi-chatbot

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

streamlit run app.py
```

## Project Structure

```sh
moreshwarnabar-udi-chatbot/
├── app.py                   # Main Streamlit application
├── requirements.txt          # Required dependencies
├── assets/                   # UI-related assets
├── services/                 # Backend services
│   ├── aws_client.py         # AWS client setup
│   ├── document_upload.py    # Document upload and processing
│   └── response_generator.py # AI response generation
├── utils/                    # Utility functions
│   ├── chat_helpers.py       # Conversation formatting helpers
│   ├── constants.py          # Application constants
│   └── layout.py             # UI layout utilities
```

## Usage

1. Start the application.
2. Upload documents (PDF, TXT, DOCX) via the sidebar.
3. Engage in a chat with the bot to retrieve knowledge from uploaded documents.
4. The chatbot will provide AI-generated responses using AWS Bedrock.

## AWS Configuration

Ensure that you have AWS credentials configured and permissions granted for:

- Amazon S3 (for document storage)
- AWS Bedrock (for AI-powered responses)

## License

This project is licensed under the MIT License.
