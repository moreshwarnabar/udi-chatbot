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
    <div className="flex gap-2 mt-4">
      <Input
        type="text"
        placeholder="Ask a question..."
        value={input}
        onChange={onChangeHandler}
      />
      <Button onClick={onClickHandler}>Send</Button>
    </div>
  );
};

export default ChatInput;
