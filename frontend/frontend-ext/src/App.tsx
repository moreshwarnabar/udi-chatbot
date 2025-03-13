import { useState } from 'react';
import OpenChatButton from './components/OpenChatButton';
import ChatWindow from './components/ChatWindow';
import { Message } from './types';

const App = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: 'system', content: 'Hello! How can I help you?' },
  ]);

  return (
    <div className="fixed bottom-4 right-4">
      {!isOpen ? (
        <OpenChatButton onClick={() => setIsOpen(true)} />
      ) : (
        <ChatWindow
          messages={messages}
          onClose={() => setIsOpen(false)}
          updateMessages={(message: string, role: 'system' | 'user') =>
            setMessages(prev => [...prev, { role, content: message }])
          }
        />
      )}
    </div>
  );
};

export default App;
