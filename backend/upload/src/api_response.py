import json
from typing import Dict, Any

class APIResponse:
    @staticmethod
    def success(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a success response.
        
        Args:
            data: The response data
            
        Returns:
            Dict containing the formatted success response
        """
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(data)
        }
    
    @staticmethod
    def error(message: str, status_code: int = 500) -> Dict[str, Any]:
        """
        Create an error response.
        
        Args:
            message: The error message
            status_code: HTTP status code (default: 500)
            
        Returns:
            Dict containing the formatted error response
        """
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Internal server error' if status_code == 500 else message,
                'error': message
            })
        } 