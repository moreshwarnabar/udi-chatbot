import json
import logging
from src.request_handler import RequestHandler
from src.api_response import APIResponse

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
        logger.info("Received file upload request")
        
        # Parse the request body
        if 'body' not in event:
            return APIResponse.error("No body found in the request", 400)
            
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        
        # Process the request
        handler = RequestHandler()
        try:
            success, result = handler.process_upload_request(body)
            return APIResponse.success(result)
        except ValueError as ve:
            return APIResponse.error(str(ve), 400)
            
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return APIResponse.error(str(e)) 