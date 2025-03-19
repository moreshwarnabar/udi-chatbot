import { useState } from 'react';
import { Message } from '@/types';
import ChatWindow from '@/components/ChatWindow';
import Toolbar from '@/components/toolbar/Toolbar';
import Navbar from '@/components/Navbar';

const App = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'Hello! How can I help you?',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
  };

  const handleLogin = () => {
    if (!isLoggedIn) {
      console.log('Logging in...');
    } else {
      console.log('Logging out...');
    }

    setIsLoggedIn(!isLoggedIn);
  };

  return (
    <>
      <div className="flex flex-col h-screen">
        <Navbar isLoggedIn={isLoggedIn} loginHandler={handleLogin} />
        <main className="flex flex-1 gap-4 p-4">
          <Toolbar />

          <div className="flex-1 flex flex-col shadow-lg rounded-xl p-4">
            <ChatWindow
              messages={messages}
              input={input}
              inputHandler={e => setInput(e.target.value)}
              sendMessageHandler={handleSendMessage}
            />
          </div>
        </main>
      </div>
    </>
  );
};

export default App;
