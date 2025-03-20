import { ValidatedFileUploadForm } from '@/types';

const getFileType = (file: File): string => {
  const extension = file.name.split('.').pop()?.toLowerCase();
  const mimeTypes: { [key: string]: string } = {
    txt: 'text/plain',
    pdf: 'application/pdf',
    doc: 'application/msword',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    rtf: 'application/rtf',
    odt: 'application/vnd.oasis.opendocument.text',
    html: 'text/html',
    htm: 'text/html',
    csv: 'text/csv',
    json: 'application/json',
    xml: 'application/xml',
    md: 'text/markdown',
    markdown: 'text/markdown',
  };

  return extension
    ? mimeTypes[extension] || file.type || 'application/octet-stream'
    : 'application/octet-stream';
};

export const getPresignedUrl = async (formData: ValidatedFileUploadForm) => {
  const url =
    'https://1r0lw223rc.execute-api.us-east-1.amazonaws.com/dev/presignedUrl';
  const headers = {
    'Content-Type': 'application/json',
  };
  const body = {
    filename: formData.file.name,
    fileType: getFileType(formData.file),
    metadata: {
      category: formData.category,
      tags: JSON.stringify(formData.tags),
    },
  };

  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error('Failed to get the presigned url');
  }

  const data = await response.json();
  if (!data['url']) {
    throw new Error('Failed to get the presigned url');
  }

  return data['url'];
};

export const uploadFileToS3 = async (url: string, file: File) => {
  try {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': file.type,
        'x-amz-acl': 'private',
        'Cache-Control': 'no-cache',
      },
      body: file,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Failed to upload file to S3: ${response.status} ${response.statusText} - ${errorText}`
      );
    }

    if (response.status !== 200) {
      throw new Error(`Unexpected response status: ${response.status}`);
    }

    return response;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`S3 upload failed: ${error.message}`);
    }
    throw new Error('S3 upload failed with unknown error');
  }
};
