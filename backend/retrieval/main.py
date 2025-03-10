import os
import json
import boto3
from dotenv import load_dotenv
from src.retriever import retrieve_data

load_dotenv()

region = os.getenv('AWS_REGION')
bedrock_runtime_client = boto3.client('bedrock-agent-runtime', region_name=region)
lambda_client = boto3.client('lambda', region_name=region)

def lambda_handler(event, context):
    body = json.loads(event['body'])

    print(f"BODY:\n {body}")
    query = body.get('query')
    msg_history = body.get('msgHistory')
    session_id = body.get('sessionId')

    retrieved_data = retrieve_data(bedrock_runtime_client, msg_history, query)

    payload = {
        "body": {
            'retrievedData': retrieved_data,
            'query': query,
            'msgHistory': msg_history,
            'sessionId': session_id
        }
    }

    response = lambda_client.invoke(
        FunctionName="udi-generator",
        Payload=json.dumps(payload),
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }