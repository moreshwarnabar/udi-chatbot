import { useState } from 'react';
import ChatHeader from './ChatHeader';
import ChatInput from './ChatInput';

interface ChatWindowProps {
  onClose: () => void;
}

const ChatWindow = ({ onClose }: ChatWindowProps) => {
  const [messages, setMessages] = useState<string[]>([
    'Hello! How can I help you?',
  ]);

  const handleSendMessage = (message: string) => {
    setMessages(prev => [...prev, message]);
  };

  return (
    <div className="w-80 h-96 bg-gray-100 shadow-xl rounded-lg flex flex-col">
      <ChatHeader onClose={onClose} />
      <div className="flex-1 p-3 overflow-y-auto">
        {messages.map((msg, idx) => (
          <p key={idx} className="text-sm text-gray-500">
            {msg}
          </p>
        ))}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWindow;
