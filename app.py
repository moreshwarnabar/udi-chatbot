import boto3
import streamlit as st

from PIL import Image

def generate_response(conversation_history, query):
    region = 'us-east-1'
    bedrock_agent_client = boto3.client('bedrock-agent-runtime',
                                        region_name=region)
    model_arn = 'arn:aws:bedrock:us-east-1:992382716564:inference-profile/us.meta.llama3-1-8b-instruct-v1:0'

    context = "\n".join(
        [f"{msg['role'].capitalize()}:{msg['content']}" for msg in conversation_history]
    )

    template = f"""Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Previous Conversation: {context}

    Question: {query}

    Helpful Answer:"""
    
    response = bedrock_agent_client.retrieve_and_generate(
        input={
            'text': template
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'DOZZ9VZFCM',
                'modelArn': model_arn
            }
        }
    )

    return response['output']['text']

# Streamlit Interface with Custom Layout and Styling
image_path = 'assets/ASU.png'  # Path to the logo/image

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
        response = generate_response(st.session_state.messages, prompt)
    
    # Display assistant's response
    with st.chat_message("assistant", avatar='assets/asu-logo.jpeg'):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})