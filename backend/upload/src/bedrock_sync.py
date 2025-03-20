import os
import time
import json
import logging
import boto3
from dataclasses import dataclass
from functools import wraps
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from botocore.exceptions import (
    ClientError,
    ValidationError,
    ParamValidationError,
    WaiterError,
    ConnectionError,
    ReadTimeoutError
)

# Load environment variables
load_dotenv()

@dataclass
class BedrockConfig:
    """Configuration for Bedrock knowledge base."""
    region: str
    knowledge_base_id: str
    data_source_id: str
    
    @classmethod
    def from_env(cls) -> 'BedrockConfig':
        """Create configuration from environment variables."""
        region = os.getenv('AWS_REGION')
        knowledge_base_id = os.getenv('KNOWLEDGE_BASE_ID')
        data_source_id = os.getenv('DATA_SOURCE_ID')
        
        if not all([region, knowledge_base_id, data_source_id]):
            missing = []
            if not region: missing.append('AWS_REGION')
            if not knowledge_base_id: missing.append('KNOWLEDGE_BASE_ID')
            if not data_source_id: missing.append('DATA_SOURCE_ID')
            raise BedrockValidationError(f"Missing required environment variables: {', '.join(missing)}")
        
        return cls(
            region=region,
            knowledge_base_id=knowledge_base_id,
            data_source_id=data_source_id
        )

class StructuredLogger:
    """Structured logging wrapper."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Add JSON formatter if not already added
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(JsonFormatter())
            self.logger.addHandler(handler)
    
    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method with structured data."""
        extra = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'service': 'bedrock-sync',
            **kwargs
        }
        self.logger.log(level, message, extra=extra)
    
    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            'timestamp': record.created,
            'level': record.levelname,
            'message': record.getMessage(),
            'service': getattr(record, 'service', 'bedrock-sync'),
            **getattr(record, 'extra', {})
        }
        
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
            
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

class BedrockSyncError(Exception):
    """Base exception for Bedrock sync errors."""
    pass

class BedrockValidationError(BedrockSyncError):
    """Exception for validation errors."""
    pass

class BedrockConnectionError(BedrockSyncError):
    """Exception for connection errors."""
    pass

class BedrockTimeoutError(BedrockSyncError):
    """Exception for timeout errors."""
    pass

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0
):
    """
    Retry decorator with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            logger = args[0].logger if args else StructuredLogger(__name__)
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, ReadTimeoutError) as e:
                    last_exception = e
                    if attempt == max_retries:
                        raise BedrockConnectionError(f"Failed after {max_retries} retries: {str(e)}")
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed: {str(e)}. "
                        f"Retrying in {delay} seconds...",
                        attempt=attempt + 1,
                        max_attempts=max_retries + 1,
                        delay=delay,
                        error=str(e)
                    )
                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)
            
            raise last_exception
        return wrapper
    return decorator

class BedrockKnowledgeBase:
    def __init__(self):
        """Initialize the Bedrock knowledge base client with configuration."""
        self.config = BedrockConfig.from_env()
        self.logger = StructuredLogger(__name__)
        
        try:
            self.bedrock = boto3.client(
                service_name='bedrock-agent',
                region_name=self.config.region
            )
            self.logger.info(
                "Bedrock client initialized successfully",
                region=self.config.region,
                knowledge_base_id=self.config.knowledge_base_id
            )
        except Exception as e:
            self.logger.error(
                "Failed to initialize Bedrock client",
                error=str(e),
                region=self.config.region
            )
            raise BedrockConnectionError(f"Failed to initialize Bedrock client: {str(e)}")
    
    def _handle_bedrock_error(self, error: Exception) -> Dict[str, Any]:
        """
        Handle Bedrock API errors and classify them appropriately.
        
        Args:
            error: The exception to handle
            
        Returns:
            Dict containing error information
        """
        error_data = {
            'error_type': type(error).__name__,
            'error_message': str(error)
        }
        
        if isinstance(error, (ValidationError, ParamValidationError)):
            self.logger.error("Validation error occurred", **error_data)
            raise BedrockValidationError(f"Invalid parameters: {str(error)}")
        elif isinstance(error, ConnectionError):
            self.logger.error("Connection error occurred", **error_data)
            raise BedrockConnectionError(f"Connection error: {str(error)}")
        elif isinstance(error, ReadTimeoutError):
            self.logger.error("Timeout error occurred", **error_data)
            raise BedrockTimeoutError(f"Request timed out: {str(error)}")
        elif isinstance(error, ClientError):
            error_code = error.response['Error']['Code']
            error_message = error.response['Error']['Message']
            error_data.update({
                'error_code': error_code,
                'error_message': error_message
            })
            
            if error_code in ['ThrottlingException', 'TooManyRequestsException']:
                self.logger.error("Rate limit exceeded", **error_data)
                raise BedrockConnectionError(f"Rate limit exceeded: {error_message}")
            elif error_code in ['ValidationException', 'InvalidParameterException']:
                self.logger.error("Invalid parameters", **error_data)
                raise BedrockValidationError(f"Invalid parameters: {error_message}")
            else:
                self.logger.error("Bedrock API error", **error_data)
                raise BedrockSyncError(f"Bedrock API error ({error_code}): {error_message}")
        else:
            self.logger.error("Unexpected error occurred", **error_data)
            raise BedrockSyncError(f"Unexpected error: {str(error)}")
    
    @retry_with_backoff(max_retries=3, initial_delay=1.0, max_delay=10.0)
    def sync_knowledge_base(self) -> Dict[str, Any]:
        """
        Trigger a synchronization of the knowledge base with the S3 data source.
        
        Returns:
            dict: Response containing sync job information
            
        Raises:
            BedrockValidationError: If parameters are invalid
            BedrockConnectionError: If connection issues occur
            BedrockTimeoutError: If request times out
            BedrockSyncError: For other Bedrock-related errors
        """
        try:
            self.logger.info(
                "Starting knowledge base sync",
                knowledge_base_id=self.config.knowledge_base_id,
                data_source_id=self.config.data_source_id
            )
            
            response = self.bedrock.start_ingestion_job(
                knowledgeBaseId=self.config.knowledge_base_id,
                dataSourceId=self.config.data_source_id
            )
            
            job_id = response['ingestionJob']['ingestionJobId']
            self.logger.info(
                "Sync job started successfully",
                job_id=job_id,
                knowledge_base_id=self.config.knowledge_base_id
            )
            
            return {
                'status': 'success',
                'job_id': job_id,
                'started_at': response['ingestionJob']['startTime']
            }
            
        except Exception as e:
            self.logger.error(
                "Failed to sync knowledge base",
                error=str(e),
                knowledge_base_id=self.config.knowledge_base_id
            )
            return self._handle_bedrock_error(e)
    
    @retry_with_backoff(max_retries=2, initial_delay=1.0, max_delay=5.0)
    def get_sync_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a knowledge base sync job.
        
        Args:
            job_id: The ID of the ingestion job
            
        Returns:
            dict: Status information about the sync job
            
        Raises:
            BedrockValidationError: If parameters are invalid
            BedrockConnectionError: If connection issues occur
            BedrockTimeoutError: If request times out
            BedrockSyncError: For other Bedrock-related errors
        """
        try:
            response = self.bedrock.get_ingestion_job(
                knowledgeBaseId=self.config.knowledge_base_id,
                ingestionJobId=job_id
            )
            
            job_status = response['ingestionJob']
            status_info = {
                'status': job_status['status'],
                'started_at': job_status['startTime'],
                'completed_at': job_status.get('completionTime'),
                'error_message': job_status.get('errorMessage')
            }
            
            self.logger.info(
                "Retrieved sync job status",
                job_id=job_id,
                status=status_info['status'],
                knowledge_base_id=self.config.knowledge_base_id
            )
            return status_info
            
        except Exception as e:
            self.logger.error(
                "Failed to get sync status",
                job_id=job_id,
                error=str(e),
                knowledge_base_id=self.config.knowledge_base_id
            )
            return self._handle_bedrock_error(e)