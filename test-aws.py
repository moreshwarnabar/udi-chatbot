import boto3

region = 'us-east-1'
bedrock_agent_client = boto3.client('bedrock-agent-runtime',
                                    region_name=region)
model_id = 'us.meta.llama3-1-8b-instruct-v1:0'
model_arn = 'arn:aws:bedrock:us-east-1:992382716564:inference-profile/us.meta.llama3-1-8b-instruct-v1:0'

query = 'What are the components of agility?'
response = bedrock_agent_client.retrieve_and_generate(
    input={
        'text': query
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'DOZZ9VZFCM',
            'modelArn': model_arn
        }
    }
)

generated_text = response['output']['text']

print(response)