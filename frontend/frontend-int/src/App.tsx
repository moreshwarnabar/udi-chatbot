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
    <div className="flex flex-col items-center justify-center min-h-svh">
      <ChatWindow messages={messages} />
      <ChatInput
        input={input}
        onChangeHandler={e => setInput(e.target.value)}
        onClickHandler={handleSendMessage}
      />
      <UploadFile file={file} fileUploadHandler={handleFileUpload} />
    </div>
  );
};

export default App;
