import { Card, CardContent } from '@/components/ui/card';
import { Message } from '@/types';
import ChatInput from '@/components/ChatInput';

interface ChatWindowProps {
  messages: Message[];
  input: string;
  inputHandler: (e: React.ChangeEvent<HTMLInputElement>) => void;
  sendMessageHandler: () => void;
}

const ChatWindow = ({
  messages,
  input,
  inputHandler,
  sendMessageHandler,
}: ChatWindowProps) => {
  return (
    <Card className="flex-1 justify-between overflow-auto pt-4 border rounded-lg">
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
      <ChatInput
        input={input}
        onChangeHandler={inputHandler}
        onClickHandler={sendMessageHandler}
      />
    </Card>
  );
};

export default ChatWindow;
