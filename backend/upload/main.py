import json
import logging
from src.request_handler import RequestHandler
from src.api_response import APIResponse

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler function that triggers Bedrock knowledge base synchronization.
    
    Args:
        event (dict): The event data passed to the Lambda function
        context (object): The Lambda context object
    
    Returns:
        dict: Response containing statusCode and body
    """
    try:
        logger.info("Received knowledge base sync request")
        
        # Process the request
        handler = RequestHandler()
        try:
            success, result = handler.trigger_kb_sync()
            return APIResponse.success(result)
        except ValueError as ve:
            return APIResponse.error(str(ve), 400)
            
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return APIResponse.error(str(e)) 