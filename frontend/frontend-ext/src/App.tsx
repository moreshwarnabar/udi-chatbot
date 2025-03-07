import { useState } from 'react';
import OpenChatButton from './components/OpenChatButton';
import ChatWindow from './components/ChatWindow';

const App = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-4 right-4">
      {!isOpen ? (
        <OpenChatButton onClick={() => setIsOpen(true)} />
      ) : (
        <ChatWindow onClose={() => setIsOpen(false)} />
      )}
    </div>
  );
};

export default App;
