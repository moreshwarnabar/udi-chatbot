import os
import logging
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()

class BedrockKnowledgeBase:
    def __init__(self):
        """
        Initialize the Bedrock knowledge base client with credentials from environment variables.
        Required env vars:
        - AWS_REGION
        - KNOWLEDGE_BASE_ID
        - S3_BUCKET_NAME (for data source)
        """
        self.region = os.getenv('AWS_REGION')
        self.knowledge_base_id = os.getenv('KNOWLEDGE_BASE_ID')
        self.data_source_id = os.getenv('DATA_SOURCE_ID')
        
        if not all([self.region, self.knowledge_base_id, self.data_source_id]):
            raise ValueError("Missing required environment variables")
        
        self.bedrock = boto3.client(
            service_name='bedrock-agent',
            region_name=self.region
        )
    
    def sync_knowledge_base(self):
        """
        Trigger a synchronization of the knowledge base with the S3 data source.
        
        Returns:
            dict: Response from the Bedrock service
        """
        try:
            logger.info(f"Starting knowledge base sync for ID: {self.knowledge_base_id}")
            
            response = self.bedrock.start_ingestion_job(
                knowledgeBaseId=self.knowledge_base_id,
                dataSourceId=self.data_source_id
            )
            
            logger.info(f"Sync job started successfully. Job ID: {response['ingestionJob']['ingestionJobId']}")
            return {
                'status': 'success',
                'job_id': response['ingestionJob']['ingestionJobId']
            }
            
        except ClientError as e:
            error_message = e.response['Error']['Message']
            logger.error(f"Failed to sync knowledge base: {error_message}")
            return {
                'status': 'error',
                'message': error_message
            }
    
    def get_sync_status(self, job_id):
        """
        Get the status of a knowledge base sync job.
        
        Args:
            job_id (str): The ID of the ingestion job
            
        Returns:
            dict: Status information about the sync job
        """
        try:
            response = self.bedrock.get_ingestion_job(
                knowledgeBaseId=self.knowledge_base_id,
                ingestionJobId=job_id
            )
            
            return {
                'status': response['ingestionJob']['status'],
                'started_at': response['ingestionJob']['startTime'],
                'completed_at': response['ingestionJob'].get('completionTime'),
                'error_message': response['ingestionJob'].get('errorMessage')
            }
            
        except ClientError as e:
            logger.error(f"Failed to get sync status: {e.response['Error']['Message']}")
            return {
                'status': 'error',
                'message': e.response['Error']['Message']
            }