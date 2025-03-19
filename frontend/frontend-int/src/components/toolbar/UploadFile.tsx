import { useState, JSX } from 'react';
import { MoveLeft, Upload, Trash, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { categories, tags } from '@/utils/data';
import { FileUploadForm } from '@/types';
import { validateFileUploadForm } from '@/utils/validation';
import { uploadFile } from '@/utils/apiCalls';

interface UploadFileProps {
  onClose: () => void;
}

const UploadFile = ({ onClose }: UploadFileProps) => {
  const [form, setForm] = useState<FileUploadForm>({
    file: null,
    category: null,
    tags: [],
  });
  const [error, setError] = useState<string | null>(null);
  const [isUploadedMessage, setIsUploadedMessage] =
    useState<JSX.Element | null>(null);
  const [filteredTags, setFilteredTags] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const error = validateFileUploadForm(form);
    if (error) {
      setError(error);
      return;
    }

    try {
      const response = await uploadFile(form);
      console.log(response);
      setIsUploadedMessage(
        <p className="text-green-500">File uploaded successfully</p>
      );
    } catch (error) {
      console.error(error);
      setIsUploadedMessage(
        <p className="text-red-500">Failed to upload file</p>
      );
    } finally {
      setForm({
        file: null,
        category: null,
        tags: [],
      });
      setError(null);
    }
  };

  return (
    <div className="px-4 flex flex-col items-center gap-4">
      <div className="flex justify-between w-full">
        <h2 className="text-lg font-bold uppercase text-asu_maroon">
          Upload Documents
        </h2>
        <button
          className="hover:text-asu_maroon hover:cursor-pointer"
          onClick={onClose}
        >
          <MoveLeft size={28} />
        </button>
      </div>
      <form className="w-full flex flex-col gap-4" onSubmit={handleSubmit}>
        <div className="w-full flex justify-start items-center gap-4">
          <Input
            type="file"
            onChange={e =>
              setForm({ ...form, file: e.target.files?.[0] ?? null })
            }
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="flex items-center gap-2 cursor-pointer p-3 border rounded-lg bg-asu_blue/90 text-white hover:bg-asu_blue transition"
          >
            <Upload />
          </label>
          {form.file && (
            <div className="flex-1 flex justify-between items-center gap-2 bg-gray-300 px-3 py-3 rounded-lg">
              <span className="text-blue-600">{form.file.name}</span>
              <button
                className="hover:text-asu_maroon hover:cursor-pointer"
                onClick={() => setForm({ ...form, file: null })}
              >
                <Trash />
              </button>
            </div>
          )}
        </div>
        <div className="flex flex-col gap-2">
          <p className="font-semibold">Category</p>
          <div className="flex justify-start items-center gap-2">
            {categories.map((c, i) => (
              <div key={i} className="flex-1 flex gap-2 items-center">
                <Input
                  className="w-5 h-5 hover:cursor-pointer"
                  type="radio"
                  id={c}
                  name="category"
                  checked={form.category === c}
                  onChange={() => setForm({ ...form, category: c })}
                />
                <label htmlFor={c}>{c}</label>
              </div>
            ))}
          </div>
        </div>
        <div>
          <p className="font-semibold mb-2">Tags</p>
          <div className="flex flex-wrap gap-2">
            {form.tags.map((tag, i) => (
              <div
                key={i}
                className="flex items-center gap-1 px-2 py-1 bg-asu_maroon text-white rounded-lg"
              >
                <span>{tag}</span>
                <button
                  type="button"
                  onClick={() =>
                    setForm({ ...form, tags: form.tags.filter(t => t !== tag) })
                  }
                  className="hover:text-asu_gold hover:cursor-pointer"
                >
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>
          <div className="relative">
            <Input
              type="text"
              className="w-full mt-2 p-2 border rounded-lg"
              value={searchTerm}
              placeholder="Search tags..."
              onChange={e => {
                const searchTerm = e.target.value.toLowerCase();
                const options = tags;
                const filtered = options.filter(opt =>
                  opt.toLowerCase().includes(searchTerm)
                );
                setSearchTerm(e.target.value);
                setFilteredTags(filtered);
              }}
            />
            {filteredTags?.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-40 overflow-y-auto">
                {filteredTags.map((tag, i) => (
                  <div
                    key={i}
                    className={`p-2 hover:bg-gray-100 cursor-pointer ${
                      form.tags.includes(tag) ? 'bg-gray-100' : ''
                    }`}
                    onClick={() => {
                      if (form.tags.includes(tag)) {
                        setForm({
                          ...form,
                          tags: form.tags.filter(t => t !== tag),
                        });
                      } else {
                        setForm({
                          ...form,
                          tags: [...form.tags, tag],
                        });
                      }
                      setSearchTerm('');
                      setFilteredTags([]);
                    }}
                  >
                    {tag}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="w-full flex justify-center items-center gap-4">
          <Button
            type="submit"
            className="bg-asu_gray text-white uppercase font-semibold hover:bg-asu_blue hover:cursor-pointer transition"
          >
            upload
          </Button>
        </div>
      </form>
      {error && <p className="text-red-500">{error}</p>}
      {isUploadedMessage}
    </div>
  );
};

export default UploadFile;
