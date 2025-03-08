import os
import boto3
from dotenv import load_dotenv
from src.retriever import retrieve_data

load_dotenv()

region = os.getenv('AWS_REGION')
bedrock_runtime_client = boto3.client('bedrock-agent-runtime', region_name=region)

def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }

response = retrieve_data(bedrock_runtime_client, [], "What are the UDI design imperatives?")
print(response)