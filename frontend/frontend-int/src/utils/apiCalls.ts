import { FileUploadForm } from '@/types';

export const uploadFile = async (form: FileUploadForm) => {
  const response = await fetch('/api/upload', {
    method: 'POST',
    body: JSON.stringify(form),
  });

  if (!response.ok) {
    throw new Error('Failed to upload file');
  }

  return response.json();
};
