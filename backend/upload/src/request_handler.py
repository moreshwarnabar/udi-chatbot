import logging
from typing import Dict, Any, Tuple

from .bedrock_sync import BedrockKnowledgeBase

logger = logging.getLogger(__name__)

class RequestHandler:
    def __init__(self):
        self.kb_sync = BedrockKnowledgeBase()

    def trigger_kb_sync(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Trigger the knowledge base synchronization with Bedrock.
        
        Returns:
            Tuple[bool, Dict[str, Any]]: Success status and result data
        """
        try:
            logger.info("Triggering knowledge base sync")
            response = self.kb_sync.sync_knowledge_base()
            return True, {
                "message": "Knowledge base sync triggered successfully",
                "jobId": response['ingestionJob']['ingestionJobId']
            }
        except Exception as e:
            logger.error(f"Error triggering knowledge base sync: {str(e)}")
            return False, {"error": str(e)} 