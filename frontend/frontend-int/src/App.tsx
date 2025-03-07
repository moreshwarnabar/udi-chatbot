import { useState } from 'react';
import { Message } from './types';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';

const App = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'Hello! How can I help you?',
    },
  ]);
  const [input, setInput] = useState('');

  const handleSendMessage = () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-svh">
      <ChatWindow messages={messages} />
      <ChatInput
        input={input}
        onChangeHandler={e => setInput(e.target.value)}
        onClickHandler={handleSendMessage}
      />
    </div>
  );
};

export default App;
