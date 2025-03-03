import os
import tempfile

from utils.constants import S3_BUCKET_NAME, DATA_SOURCE_ID, KNOWLEDGE_BASE_ID

def upload_to_s3(s3_client, uploaded_file):
    """
    Uploads a document to the specified S3 bucket.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        # Generate S3 object key (file name in S3)
        s3_key = uploaded_file.name

        # Upload file to S3
        s3_client.upload_file(temp_path, S3_BUCKET_NAME, s3_key)
        print(f"Uploaded {uploaded_file.name} to S3 bucket {S3_BUCKET_NAME} with key {s3_key}")

        # Clean up temporary file
        os.remove(temp_path)

        return s3_key
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return None

def trigger_knowledge_base_sync(bedrock_client):
    """
    Triggers Bedrock to sync the knowledge base with the S3 data source.
    """
    try:
        response = bedrock_client.start_ingestion_job(
            dataSourceId=DATA_SOURCE_ID, knowledgeBaseId=KNOWLEDGE_BASE_ID
        )
        print(f"Triggered knowledge base sync: {response['ingestionJob']['status']}")
        return True
    except Exception as e:
        print(f"Error triggering knowledge base sync: {e}")
        return False

def process_document(bedrock_client, s3_client, uploaded_file):
    """
    Handles the end-to-end process: upload to S3 and trigger knowledge base sync.
    """
    # s3_key = upload_to_s3(s3_client, uploaded_file)
    s3_key = True
    if s3_key:
        sync_status = trigger_knowledge_base_sync(bedrock_client)
        return sync_status
    return False