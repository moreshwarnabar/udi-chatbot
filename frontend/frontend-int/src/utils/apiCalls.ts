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

export const uploadFile = async (form: ValidatedFileUploadForm) => {
  const url =
    'https://1r0lw223rc.execute-api.us-east-1.amazonaws.com/dev/presignedUrl';
  const headers = {
    'Content-Type': 'application/json',
  };
  const body = {
    filename: form.file.name,
    fileType: getFileType(form.file),
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
