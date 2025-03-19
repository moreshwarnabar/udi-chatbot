import { useState } from 'react';

interface ChatInputProps {
  isFetching: boolean;
  onSendMessage: (message: string) => void;
}

const ChatInput = ({ isFetching, onSendMessage }: ChatInputProps) => {
  const [message, setMessage] = useState('');

  const handleMessage = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="p-2 flex bg-gray-100">
      <input
        className="w-full px-3 py-2 border rounded-3xl outline-none focus:ring-0 focus:border-gray-300"
        type="text"
        placeholder={
          isFetching ? 'Crafting your answer...' : 'Type your message...'
        }
        disabled={isFetching}
        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleMessage()}
      />
    </div>
  );
};

export default ChatInput;
