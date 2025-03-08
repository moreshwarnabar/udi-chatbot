import React from 'react';
import { Input } from '@/components/ui/input';
import { Button } from './ui/button';

interface ChatInputProps {
  input: string;
  onChangeHandler: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onClickHandler: () => void;
}

const ChatInput = ({
  input,
  onChangeHandler,
  onClickHandler,
}: ChatInputProps) => {
  return (
    <div className="flex gap-4 mx-4">
      <Input
        type="text"
        placeholder="Ask a question..."
        value={input}
        onChange={onChangeHandler}
        className="border rounded-lg p-3"
      />
      <Button
        className="bg-blue-500 hover:bg-blue-600 hover:cursor-pointer text-white px-4 py-2 rounded-lg"
        onClick={onClickHandler}
      >
        Send
      </Button>
    </div>
  );
};

export default ChatInput;
