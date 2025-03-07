import { MessageSquare } from 'lucide-react';

interface OpenChatButtonProps {
  onClick: () => void;
}

const OpenChatButton = ({ onClick }: OpenChatButtonProps) => {
  return (
    <button
      className="bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 hover:cursor-pointer transition"
      onClick={onClick}
    >
      <MessageSquare size={24} />
    </button>
  );
};

export default OpenChatButton;
