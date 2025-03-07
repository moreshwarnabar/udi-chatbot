import { useState } from 'react';
import ChatHeader from './ChatHeader';
import ChatInput from './ChatInput';

interface ChatWindowProps {
  onClose: () => void;
}

interface Message {
  role: 'system' | 'user';
  content: string;
}

const ChatWindow = ({ onClose }: ChatWindowProps) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'system', content: 'Hello! How can I help you?' },
  ]);

  const handleSendMessage = (message: string) => {
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    setTimeout(() => {
      setMessages(prev => [
        ...prev,
        { role: 'system', content: "I'm a chatbot. I'm here to help you!" },
      ]);
    }, 1000);
  };

  return (
    <div className="w-80 h-96 bg-gray-100 shadow-xl rounded-lg flex flex-col">
      <ChatHeader onClose={onClose} />
      <div className="flex-1 p-3 overflow-y-auto space-y-2">
        {messages.map((msg, idx) => (
          <p
            key={idx}
            className={`text-sm p-2 max-w-[75%] rounded-lg ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white self-end ml-auto'
                : 'bg-gray-200 text-black self-start'
            }`}
          >
            {msg.content}
          </p>
        ))}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWindow;
