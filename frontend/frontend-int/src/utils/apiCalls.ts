import { ValidatedFileUploadForm } from '@/types';

const extractFileContent = async (file: File): Promise<string> => {
  return await new Promise(resolve => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = reader.result?.toString().split(',')[1] || '';
      resolve(base64String);
    };
    reader.readAsDataURL(file);
  });
};

export const uploadFile = async (form: ValidatedFileUploadForm) => {
  const url =
    'https://1r0lw223rc.execute-api.us-east-1.amazonaws.com/dev/upload';
  const headers = {
    'Content-Type': 'application/json',
  };
  const body = {
    fileName: form.file.name,
    fileContent: await extractFileContent(form.file),
    category: form.category,
    tags: form.tags,
  };

  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error('Failed to upload file');
  }

  return response.json();
};
