import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
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
  const [messages, setMessages] = useState<Message[]>(() => {
    const storedMsgs = localStorage.getItem('udiChatMessages');
    return storedMsgs
      ? JSON.parse(storedMsgs)
      : [{ role: 'system', content: 'Hello! How can I help you?' }];
  });

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    localStorage.setItem('udiChatMessages', JSON.stringify(messages));
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    try {
      const response = await fetch(
        'https://1r0lw223rc.execute-api.us-east-1.amazonaws.com/dev/retrieve',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: message,
            msgHistory: messages,
            sessionId: 1,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      console.log(data.body.response);
      setMessages(prev => [
        ...prev,
        { role: 'system', content: data.body.response },
      ]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="w-120 h-128 bg-gray-100 shadow-xl rounded-lg flex flex-col">
      <ChatHeader onClose={onClose} />
      <div className="flex-1 p-3 overflow-y-auto space-y-2 max-h-[calc(100%-80px)]">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`text-sm p-2 max-w-[75%] w-fit rounded-lg ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white text-right self-end ml-auto'
                : 'bg-gray-200 text-black self-start'
            }`}
          >
            <ReactMarkdown
              components={{
                ul: ({ children }) => (
                  <ul className="list-disc pl-5">{children}</ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal pl-5">{children}</ol>
                ),
                li: ({ children }) => <li className="pl-2">{children}</li>,
              }}
            >
              {msg.content}
            </ReactMarkdown>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWindow;
