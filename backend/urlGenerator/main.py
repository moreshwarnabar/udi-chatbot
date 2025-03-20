import os
import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Get bucket name from environment variable
    bucket_name = os.environ.get('AWS_BUCKET_NAME')
    
    # Extract file details from request
    try:
        body = json.loads(event['body'])
        file_name = body['filename']
        file_type = body['fileType']
    except (KeyError, TypeError):
        return {
            'statusCode': 400,
            'body': 'Missing required parameters: filename and fileType'
        }

    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_name,
                'ContentType': file_type
            },
            ExpiresIn=300  # URL expires in 5 minutes
        )

        payload = {
            'url': presigned_url,
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,PUT'
            },
            'body': json.dumps(payload)
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f'Error generating presigned URL: {str(e)}'
        }
