from dotenv import load_dotenv
from src.generator import GeneratorAgent

load_dotenv()

def lambda_handler(event, context):
    body = event['body']\

    retrieved_data = body.get('retrievedData')
    query = body.get('query')
    msg_history = body.get('msgHistory')
    session_id = body.get('sessionId')

    context = "\n".join(
        [item['content']['text'] for item in retrieved_data]
    )

    agent = GeneratorAgent()
    reply: str = agent.generate_response(query, context)

    msg_history.extend([
        {'role': 'user', 'content': query},
        {'role': 'system', 'content': reply}
    ])

    payload = {
        "response": reply,
        "msgHistory": msg_history,
        "sessionId": session_id
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": payload
    }