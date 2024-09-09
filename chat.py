import os
import random
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from PIL import Image

def load_docs(file_paths):
    # Load documents from all PDFs
    docs = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path=file_path)
        docs.extend(loader.load())  # Add the loaded documents to the list

    return docs

def split_docs(docs):
    # Split the document text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)

    return all_splits

def store_docs(all_splits):
    vectorstore = Chroma.from_documents(
        documents=all_splits, embedding=OpenAIEmbeddings())
    
    return vectorstore

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_response(vectorstore, query):
    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 6})
    llm = ChatOpenAI(model='gpt-4o-mini')

    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}

    Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    for chunk in rag_chain.stream(query):
        yield chunk

def setup_vectorstore():
    # Define file paths (update these to match your document locations)
    file_paths = ['data/doc-a.pdf', 'data/doc-b.pdf', 'data/doc-c.pdf']

    # Load and split documents
    docs = load_docs(file_paths)
    all_splits = split_docs(docs)

    # Store splits in a vector store
    vectorstore = store_docs(all_splits)

    return vectorstore

# Streamlit Interface with Custom Layout and Styling
image_path = 'assets/asu.png'  # Path to the logo/image

col1, mid, col2 = st.columns([1, 1, 12])
with col1:
    image = Image.open(image_path)
    st.image(image, width=100)
with col2:
    st.title("University Design Institute")

st.subheader("Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Preload vectorstore when the app starts
vectorstore = setup_vectorstore()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user", avatar="assets/user.jpeg"):
        st.markdown(prompt)

    # Generate the response using your RAG logic
    with st.spinner(text="In progress..."):
        response = ""
        for chunk in generate_response(vectorstore, prompt):
            response += chunk
    
    # Display assistant's response
    with st.chat_message("assistant", avatar='assets/asu-logo.jpeg'):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})