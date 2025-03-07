import { X } from 'lucide-react';

interface ChatHeaderProps {
  onClose: () => void;
}

const ChatHeader = ({ onClose }: ChatHeaderProps) => {
  return (
    <div className="flex justify-between items-center bg-blue-600 text-white p-3 rounded-t-lg">
      <span>Chatbot</span>
      <button className="hover:cursor-pointer" onClick={onClose}>
        <X size={20} />
      </button>
    </div>
  );
};

export default ChatHeader;
