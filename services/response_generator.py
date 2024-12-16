from services.aws_client import get_bedrock_client

def generate_response(conversation_history, query):
    region = 'us-east-1'
    bedrock_agent_client = get_bedrock_client(region)
    model_arn = 'arn:aws:bedrock:us-east-1:992382716564:inference-profile/us.meta.llama3-1-8b-instruct-v1:0'

    context = "\n".join(
        [f"{msg['role'].capitalize()}:{msg['content']}" for msg in conversation_history]
    )

    template = f"""
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Previous Conversation: {context}

    Question: {query}

    Helpful Answer:
    """
    
    response = bedrock_agent_client.retrieve_and_generate(
        input={'text': template},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'DOZZ9VZFCM',
                'modelArn': model_arn
            }
        }
    )

    return response['output']['text']