import os

def retrieve_data(client, msg_history, query):
    context = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in msg_history] + [f"user: {query}"]
    )

    response = client.retrieve(
        knowledgeBaseId=os.getenv('KNOWLEDGE_BASE_ID'),
        retrievalQuery={'text': context},
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': 3
            }
        }
    )

    return response['retrievalResults'];