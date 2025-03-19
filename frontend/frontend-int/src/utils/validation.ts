import { FileUploadForm } from '@/types';

export const validateFileUploadForm = (form: FileUploadForm) => {
  if (!form.file) {
    return 'Please upload a file';
  }
  if (!form.category) {
    return 'Please select a category';
  }
  if (form.tags.length === 0) {
    return 'Please select at least one tag';
  }
  return null;
};
