import os
import boto3
from dotenv import load_dotenv
from typing import Optional, Tuple, Dict, Any
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

class S3Uploader:
    def __init__(self):
        """Initialize S3 client with credentials from environment variables."""
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.region = os.getenv('AWS_REGION', 'us-east-1')

        self.s3_client = boto3.client(
            's3',
            region_name=self.region
        )

    def upload_file(
        self, 
        file_path: str, 
        object_name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Upload a file to an S3 bucket with optional metadata and content type.

        Args:
            file_path (str): Path to the file to upload
            object_name (str, optional): S3 object name. If not specified, file_path's basename is used
            metadata (Dict[str, str], optional): Metadata to attach to the S3 object
            content_type (str, optional): The content type of the file. If not specified, will use application/octet-stream

        Returns:
            tuple: (success (bool), message (str))
                  If successful, message contains the S3 URL
                  If unsuccessful, message contains the error description
        """
        # If S3 object_name was not specified, use file_path's basename
        if object_name is None:
            object_name = os.path.basename(file_path)

        # Prepare the upload parameters
        extra_args = {}
        
        # Add metadata if provided
        if metadata:
            extra_args['Metadata'] = metadata
            
        # Add content type if provided, otherwise use default
        extra_args['ContentType'] = content_type or 'application/octet-stream'

        try:
            # Upload the file with extra arguments
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                object_name,
                ExtraArgs=extra_args
            )
            
            # Generate the URL for the uploaded file
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{object_name}"
            return True, url
            
        except FileNotFoundError:
            return False, f"The file {file_path} was not found"
        except ClientError as e:
            return False, f"An error occurred: {str(e)}"