import base64
import os
import tempfile
import mimetypes

def save_temp_file(file_content: str, filename: str) -> str:
    """Save base64 encoded content to a temporary file."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    # Decode and write the file content
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(file_content))
    
    return file_path

def get_content_type(filename: str) -> str:
    """Determine the content type based on the file extension."""
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or 'application/octet-stream'