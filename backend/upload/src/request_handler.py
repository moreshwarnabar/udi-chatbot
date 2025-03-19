import json
import logging
import os
from typing import Dict, Any, Tuple

from .s3_upload import S3Uploader
from .utils import save_temp_file, get_content_type
from .bedrock_sync import BedrockKnowledgeBase

logger = logging.getLogger(__name__)

class RequestHandler:
    def __init__(self):
        self.s3_uploader = S3Uploader()
        self.kb_sync = BedrockKnowledgeBase()

    def validate_request(self, body: Dict[str, Any]) -> None:
        """
        Validate the request body contains all required fields.
        
        Args:
            body: The request body to validate
            
        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ['filename', 'fileContent', 'category', 'tags']
        missing_fields = [field for field in required_fields if field not in body]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    def prepare_metadata(self, category: str, tags: list) -> Dict[str, str]:
        """
        Prepare metadata for S3 upload.
        
        Args:
            category: The category of the file
            tags: List of tags associated with the file
            
        Returns:
            Dict containing the prepared metadata
        """
        return {
            'category': category,
            'tags': ','.join(tags) if isinstance(tags, list) else tags
        }

    def sync_knowledge_base(self) -> None:
        """
        Synchronize the knowledge base with Bedrock.
        """
        try:
            sync_result = self.kb_sync.sync_knowledge_base()
            if sync_result['status'] != 'success':
                logger.warning(f"Knowledge base sync failed: {sync_result.get('message', 'Unknown error')}")
        except Exception as bedrock_error:
            logger.warning(f"Failed to sync knowledge base: {str(bedrock_error)}")

    def process_upload_request(self, body: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Process the file upload request.
        
        Args:
            body: The request body containing file information
            
        Returns:
            Tuple containing success status and response data
        """
        self.validate_request(body)
        
        filename = body['filename']
        file_content = body['fileContent']
        category = body['category']
        tags = body['tags']
        
        temp_file_path = save_temp_file(file_content, filename)
        
        try:
            metadata = self.prepare_metadata(category, tags)
            content_type = get_content_type(filename)
            
            success, result = self.s3_uploader.upload_file(
                file_path=temp_file_path,
                object_name=filename,
                metadata=metadata,
                content_type=content_type
            )
            
            if not success:
                raise Exception(result)
            
            os.remove(temp_file_path)
            self.sync_knowledge_base()
            
            return True, {
                'message': 'File uploaded successfully',
                'url': result,
                'metadata': metadata
            }
            
        except Exception as upload_error:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise upload_error 