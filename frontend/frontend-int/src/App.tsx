import { useState } from 'react';
import { Message } from './types';
import ChatWindow from './components/ChatWindow';
import UploadFile from './components/UploadFile';
import PastChats from './components/PastChats';
import Navbar from './components/Navbar';

const App = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'Hello! How can I help you?',
    },
  ]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleSendMessage = () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
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
      <div className="flex flex-col h-screen gap-4">
        <Navbar isLoggedIn={isLoggedIn} loginHandler={handleLogin} />
        <main className="flex flex-1 gap-4 pr-4 pl-4">
          <div className="w-1/4 p-4 border shadow-lg rounded-xl">
            <UploadFile file={file} fileUploadHandler={handleFileUpload} />
            <PastChats />
          </div>
          <div className="w-3/4 flex flex-col shadow-lg rounded-xl p-4">
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
