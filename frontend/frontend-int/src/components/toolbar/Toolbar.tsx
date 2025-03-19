import { useState } from 'react';
import { Wrench, Upload, MessagesSquare } from 'lucide-react';
import UploadFile from '@/components/toolbar/UploadFile';
import ChatHistory from '@/components/toolbar/ChatHistory';

const Toolbar = () => {
  const [isOpen, setIsOpen] = useState<'UPLOAD' | 'PAST_CHATS' | 'NONE'>(
    'NONE'
  );

  const tools = [
    {
      id: 'UPLOAD',
      icon: <Upload size={32} />,
      component: <UploadFile onClose={() => setIsOpen('NONE')} />,
      onClick: () => setIsOpen('UPLOAD'),
    },
    {
      id: 'PAST_CHATS',
      icon: <MessagesSquare size={32} />,
      component: <ChatHistory onClose={() => setIsOpen('NONE')} />,
      onClick: () => setIsOpen('PAST_CHATS'),
    },
  ];

  const displayTool = tools.find(tool => tool.id === isOpen);

  return (
    <div
      className={`${
        isOpen !== 'NONE' && 'w-1/4'
      } py-4 border shadow-lg rounded-xl`}
    >
      {isOpen === 'NONE' ? (
        <div className="flex flex-col items-center gap-4">
          <Wrench />
          <div className="flex flex-col items-center bg-gray-100">
            {tools.map(t => (
              <button
                className="p-4 border border-gray-200 text-asu_maroon hover:text-asu_gold hover:cursor-pointer"
                id={t.id}
                onClick={t.onClick}
              >
                {t.icon}
              </button>
            ))}
          </div>
        </div>
      ) : (
        displayTool?.component
      )}
    </div>
  );
};

export default Toolbar;
