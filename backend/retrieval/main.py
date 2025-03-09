import os
import json
import boto3
from dotenv import load_dotenv
from src.retriever import retrieve_data

load_dotenv()

region = os.getenv('AWS_REGION')
bedrock_runtime_client = boto3.client('bedrock-agent-runtime', region_name=region)

def lambda_handler(event, context):
    body = json.loads(event['body'])

    print(f"BODY:\n {body}")
    query = body.get('query')
    msg_history = body.get('msgHistory')
    session_id = body.get('sessionId')

    response = retrieve_data(bedrock_runtime_client, msg_history, query)

    payload = {
        'retrievedData': response,
        'query': query,
        'msgHistory': msg_history,
        'sessionId': session_id
    }
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(payload)
    }