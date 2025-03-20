import { FileUploadForm, ValidatedFileUploadForm } from '@/types';

export const validateFileUploadForm = (
  form: FileUploadForm
): ValidatedFileUploadForm | string => {
  if (!form.file) {
    return 'Please upload a file';
  }
  if (!form.file.name || form.file.name.trim() === '') {
    return 'File must have a name';
  }
  if (form.file.size === 0) {
    return 'File cannot be empty';
  }
  if (!form.category) {
    return 'Please select a category';
  }
  if (form.tags.length === 0) {
    return 'Please select at least one tag';
  }
  return {
    file: form.file,
    category: form.category,
    tags: form.tags,
  };
};
