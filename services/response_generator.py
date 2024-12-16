from services.aws_client import get_bedrock_runtime_client
from utils.constants import REGION, MODEL_ARN, KNOWLEDGE_BASE_ID

def generate_response(conversation_history, query):
    bedrock_agent_client = get_bedrock_runtime_client(REGION)

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
                'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                'modelArn': MODEL_ARN
            }
        }
    )

    return response['output']['text']