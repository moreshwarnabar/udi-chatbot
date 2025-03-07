import { Input } from '@/components/ui/input';
import { Upload } from 'lucide-react';

interface UploadFileProps {
  file: File | null;
  fileUploadHandler: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const UploadFile = ({ file, fileUploadHandler }: UploadFileProps) => {
  return (
    <div className="mt-2 flex items-center gap-2">
      <Input
        type="file"
        onChange={fileUploadHandler}
        className="hidden"
        id="file-upload"
      />
      <label
        htmlFor="file-upload"
        className="flex items-center gap-2 cursor-pointer"
      >
        <Upload /> Upload Document
      </label>
      {file && <span className="text-sm text-gray-500">{file.name}</span>}
    </div>
  );
};

export default UploadFile;
