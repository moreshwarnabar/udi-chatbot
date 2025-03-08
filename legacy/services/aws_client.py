import boto3

def get_bedrock_runtime_client(region="us-east-1"):
    return boto3.client('bedrock-agent-runtime', region_name=region)

def get_bedrock_agent_client(region='us-east-1'):
    return boto3.client('bedrock-agent', region_name=region)

def get_s3_client(region='us-east-1'):
    return boto3.client('s3', region_name=region)