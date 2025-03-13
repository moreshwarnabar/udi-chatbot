import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import ChatHeader from './ChatHeader';
import ChatInput from './ChatInput';
import { Message } from '../types';
import { formatReply } from '../utils/helpers';

interface ChatWindowProps {
  messages: Message[];
  onClose: () => void;
  updateMessages: (message: string, role: 'system' | 'user') => void;
}

const ChatWindow = ({ messages, onClose, updateMessages }: ChatWindowProps) => {
  const [isFetching, setIsFetching] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    updateMessages(message, 'user');
    setIsFetching(true);

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
      const body = JSON.parse(data.body);
      const content = JSON.parse(body.response);
      console.log(content);

      const reply = formatReply(content);
      console.log(reply);
      updateMessages(reply, 'system');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsFetching(false);
    }
  };

  return (
    <div className="w-120 h-128 bg-gray-100 shadow-xl rounded-lg flex flex-col">
      <ChatHeader onClose={onClose} />
      <div className="flex-1 p-3 overflow-y-auto space-y-2 max-h-[calc(100%-80px)]">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex w-full ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`text-sm p-2 max-w-[75%] w-fit rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white self-end'
                  : 'bg-gray-200 text-black self-start'
              }`}
            >
              <ReactMarkdown
                components={{
                  p: ({ children }) => <p>{children}</p>,
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
          </div>
        ))}
        {isFetching && (
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150" />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300" />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput isFetching={isFetching} onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWindow;
