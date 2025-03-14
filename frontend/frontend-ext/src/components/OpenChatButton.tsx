import { MessageSquare } from 'lucide-react';

interface OpenChatButtonProps {
  onClick: () => void;
}

const OpenChatButton = ({ onClick }: OpenChatButtonProps) => {
  return (
    <button
      className="bg-asu_gray text-white p-3 rounded-full shadow-lg hover:bg-asu_blue hover:cursor-pointer transition"
      onClick={onClick}
    >
      <MessageSquare size={32} />
    </button>
  );
};

export default OpenChatButton;
