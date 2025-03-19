import { X } from 'lucide-react';

interface ChatHeaderProps {
  onClose: () => void;
}

const ChatHeader = ({ onClose }: ChatHeaderProps) => {
  return (
    <div className="flex justify-between items-center bg-asu_maroon text-white p-3 rounded-t-lg">
      <span className="font-bold">UDI Online Digital Assistant</span>
      <button className="hover:cursor-pointer text-asu_gold" onClick={onClose}>
        <X size={24} />
      </button>
    </div>
  );
};

export default ChatHeader;
