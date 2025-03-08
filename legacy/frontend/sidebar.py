import streamlit as st
from services.document_upload import process_document

def sidebar(s3_client, bedrock_client):
    st.sidebar.title("Document Upload")

    uploaded_file = st.sidebar.file_uploader("Upload a document (PDF, TXT, etc.)", type=["pdf", "txt", "docx"])
    category = st.sidebar.selectbox("Select a category", ["Policy", "Project"])
    tags = st.sidebar.text_input("Enter tags (comma-separated)")

    # TODO: Use LLM to generate summary

    if uploaded_file and st.sidebar.button('Upload Document'):
        with st.spinner("Uploading document..."):
            success = process_document(bedrock_client, s3_client, uploaded_file,
                                       metadata={"category": category.lower(), "tags": tags})
        if success:
            st.sidebar.success("Document uploaded and indexed successfully!")
        else:
            st.sidebar.error("Failed to upload or index the document.")