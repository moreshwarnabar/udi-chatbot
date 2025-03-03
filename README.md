# UDI Chatbot

A Streamlit-based chatbot for the University Design Institute (UDI), utilizing Retrieval-Augmented Generation (RAG) with OpenAI models and ChromaDB for document retrieval.

## Features
- Loads and processes PDFs for knowledge retrieval
-	Uses ChromaDB for vector storage and similarity-based retrieval
-	Generates responses using OpenAI’s GPT model
-	Interactive UI built with Streamlit

## Installation
1. Clone the repository:
```bash
git clone 
cd moreshwarnabar-udi-chatbot
```
2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Ensure you have the required PDF documents in the data/ directory.
2. Run the chatbot:
```bash
streamlit run chat.py
```
3. Interact with the chatbot through the Streamlit interface.

License

This project is licensed under MIT License.
