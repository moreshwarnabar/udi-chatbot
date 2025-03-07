import { Card, CardContent } from '@/components/ui/card';
import { Message } from '@/types';

const ChatWindow = ({ messages }: { messages: Message[] }) => {
  return (
    <Card className="flex-1 overflow-auto p-4">
      <CardContent>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 ${
              msg.role === 'user' ? 'text-right' : 'text-left'
            }`}
          >
            <span className="p-2 bg-gray-200 rounded-md inline-block">
              {msg.content}
            </span>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};

export default ChatWindow;
