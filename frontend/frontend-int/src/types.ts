import { categories, tags } from '@/utils/data';

type Category = (typeof categories)[number];
type Tag = (typeof tags)[number];

export interface Message {
  role: 'system' | 'user';
  content: string;
}

export interface FileUploadForm {
  file: File | null;
  category: Category | null;
  tags: Tag[];
}
