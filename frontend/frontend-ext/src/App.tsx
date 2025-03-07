import { useState } from 'react';
import { MessageSquare, X } from 'lucide-react';

const App = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="fixed bottom-4 right-4">
      {!isOpen ? (
        <button
          className="bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition"
          onClick={() => setIsOpen(true)}
        >
          <MessageSquare size={24} />
        </button>
      ) : (
        <div className="w-80 h-96 bg-white shadow-xl rounded-lg flex flex-col">
          <div>
            <span>Chatbot</span>
            <button onClick={() => setIsOpen(false)}>
              <X size={20} />
            </button>
          </div>
          <div>
            <p>Hello! How can I help you?</p>
          </div>
          <div>
            <input type="text" placeholder="Type your message..." />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
