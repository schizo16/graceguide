import { useState, useRef } from 'react';

interface Props {
  onSend: (text: string) => void;
  disabled?: boolean;
}

const SUGGESTIONS = [
  'Best early weapons',
  'How to beat Godrick',
  'Explain Radahn lore',
];

export default function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (!text.trim() || disabled) return;
    onSend(text.trim());
    setText('');
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-white/10 p-3 shrink-0">
      <div className="flex gap-2">
        <textarea
          ref={inputRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about the game... (Enter to send)"
          rows={1}
          className="flex-1 bg-white/10 rounded-lg px-3 py-2 text-sm text-white
                     placeholder-gray-600 resize-none outline-none
                     focus:ring-1 focus:ring-amber-500/50"
          disabled={disabled}
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !text.trim()}
          className="px-4 py-2 bg-amber-600 hover:bg-amber-500 disabled:bg-gray-800
                     disabled:text-gray-600 text-white rounded-lg text-sm
                     transition-colors"
        >
          Send
        </button>
      </div>

      {/* Quick suggestion chips */}
      <div className="flex gap-2 mt-2 overflow-x-auto">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => onSend(s)}
            className="text-[11px] px-2 py-1 bg-white/5 hover:bg-white/10
                       text-gray-500 hover:text-gray-300 rounded-full
                       whitespace-nowrap transition-colors"
          >
            {s} →
          </button>
        ))}
      </div>
    </div>
  );
}
