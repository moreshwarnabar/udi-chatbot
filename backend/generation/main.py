import os
import json
from dotenv import load_dotenv
from src.generator import GeneratorCrew

load_dotenv()

def lambda_handler(event, context):
    body = json.loads(event['body'])

    retrieved_data = body.get('retrieved_data')
    query = body.get('query')
    msg_history = body.get('msgHistory')
    session_id = body.get('sessionId')

    context = "\n".join(
        [item['content']['text'] for item in retrieved_data]
    )

    inputs = {
        "context": context,
        "query": query
    }

    crew = GeneratorCrew()
    response = crew.kickoff(inputs=inputs)

    msg_history.append(
        {'role': 'user', 'content': query},
        {'role': 'system', 'content': response}
    )

    payload = {
        "response": response,
        "msgHistory": msg_history,
        "sessionId": session_id
    }
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(payload)
    }