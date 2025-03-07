import { useState } from 'react';
import { Message } from './types';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import UploadFile from './components/UploadFile';

const App = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'Hello! How can I help you?',
    },
  ]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState<File | null>(null);

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

  return (
    <div className="flex h-screen p-4 gap-4">
      <div className="w-1/4 p-4 border-r">
        <UploadFile file={file} fileUploadHandler={handleFileUpload} />
      </div>
      <div className="w-3/4 flex flex-col">
        <ChatWindow messages={messages} />
        <ChatInput
          input={input}
          onChangeHandler={e => setInput(e.target.value)}
          onClickHandler={handleSendMessage}
        />
      </div>
    </div>
  );
};

export default App;
