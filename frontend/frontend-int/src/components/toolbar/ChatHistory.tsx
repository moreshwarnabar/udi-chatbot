import { MoveLeft, Ellipsis } from 'lucide-react';

interface ChatHistoryProps {
  onClose: () => void;
}

const ChatHistory = ({ onClose }: ChatHistoryProps) => {
  const chatHistory = [
    {
      id: 1,
      title: 'Planetary Health Research',
      date: 'Today',
      time: '13:52',
    },
    {
      id: 2,
      title: 'Colab Meeting',
      date: 'Yesterday',
      time: '10:30',
    },
    {
      id: 3,
      title: 'AIHEL Data Visualization',
      date: '2025-03-18',
      time: '15:45',
    },
    {
      id: 4,
      title: 'Sign out P-Card',
      date: '2025-03-17',
      time: '12:00',
    },
  ];

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="px-4 flex justify-between w-full">
        <h2 className="text-lg font-bold uppercase text-asu_maroon">
          Chat History
        </h2>
        <button
          className="hover:text-asu_maroon hover:cursor-pointer"
          onClick={onClose}
        >
          <MoveLeft size={28} />
        </button>
      </div>
      <div className="w-full flex flex-col">
        {chatHistory.map(chat => (
          <div
            key={chat.id}
            className="w-full flex flex-col gap-2 border border-gray-200 bg-gray-100 p-2"
          >
            <div className="flex gap-2 justify-between">
              <h3>{chat.title}</h3>
              <button className="hover:text-asu_gray hover:cursor-pointer">
                <Ellipsis size={16} />
              </button>
            </div>
            <div className="flex gap-2 justify-between text-sm text-gray-500">
              <p>{chat.date}</p>
              <p>{chat.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatHistory;
