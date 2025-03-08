import { Card, CardContent } from '@/components/ui/card';
import { Message } from '@/types';

const ChatWindow = ({ messages }: { messages: Message[] }) => {
  return (
    <Card className="flex-1 overflow-auto pt-4 border rounded-lg">
      <CardContent>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-2 max-w-[75%] w-fit rounded-lg ${
              msg.role === 'user'
                ? 'bg-blue-600 text-white self-end text-right ml-auto'
                : 'bg-gray-200 text-black self-start'
            }`}
          >
            <p className="p-2 rounded-md">{msg.content}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};

export default ChatWindow;
