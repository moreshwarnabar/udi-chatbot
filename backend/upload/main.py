import json
import logging
import os
from src.s3_upload import S3Uploader
from src.utils import save_temp_file, get_content_type

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler function that processes file upload requests from API Gateway.
    
    Expected request format:
    {
        "filename": "example.pdf",
        "fileContent": "base64_encoded_content",
        "category": "documents",
        "tags": ["important", "2024", "contract"]
    }
    
    Args:
        event (dict): The event data passed to the Lambda function
        context (object): The Lambda context object
    
    Returns:
        dict: Response containing statusCode and body
    """
    try:
        # Log the incoming event
        logger.info("Received file upload request")
        
        # Parse the request body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            raise ValueError("No body found in the request")
        
        # Extract required fields
        required_fields = ['filename', 'fileContent', 'category', 'tags']
        if not all(field in body for field in required_fields):
            missing_fields = [field for field in required_fields if field not in body]
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        filename = body['filename']
        file_content = body['fileContent']
        category = body['category']
        tags = body['tags']
        
        # Save the file temporarily
        temp_file_path = save_temp_file(file_content, filename)
        
        # Initialize S3 uploader
        s3_uploader = S3Uploader()
        
        # Prepare metadata
        metadata = {
            'category': category,
            'tags': ','.join(tags) if isinstance(tags, list) else tags
        }
        
        # Get content type
        content_type = get_content_type(filename)
        
        # Upload file with metadata
        try:
            success, result = s3_uploader.upload_file(
                file_path=temp_file_path,
                object_name=filename,
                metadata=metadata,
                content_type=content_type
            )
            
            if not success:
                raise Exception(result)
            
            # Clean up temporary file
            os.remove(temp_file_path)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'File uploaded successfully',
                    'url': result,
                    'metadata': metadata
                })
            }
            
        except Exception as upload_error:
            # Clean up temporary file in case of error
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise upload_error
        
    except Exception as e:
        # Log the error
        logger.error(f"Error processing event: {str(e)}")
        
        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            })
        } 