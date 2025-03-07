import { useState } from 'react';
import { Message } from './types';
import ChatWindow from './components/ChatWindow';

const App = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'Hello! How can I help you?',
    },
  ]);

  return (
    <div className="flex flex-col items-center justify-center min-h-svh">
      <ChatWindow messages={messages} />
    </div>
  );
};

export default App;
