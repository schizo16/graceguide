import { useState } from 'react';

const QUICK_ACTIONS = [
  { id: 'hint', label: '🔄 Hint me', prompt: 'Give me a hint for where to go next' },
  { id: 'area', label: '🗺️ This area?', prompt: "What's in this area? Points of interest?" },
  { id: 'build', label: '⚔️ My build', prompt: 'Show my current build recommendations' },
  { id: 'lore', label: '📖 Lore check', prompt: 'Explain the lore of this area' },
  { id: 'next', label: '🆕 What now?', prompt: "What should I do next in the game?" },
];

interface Props {
  onSendMessage: (text: string) => void;
}

export default function ControllerMode({ onSendMessage }: Props) {
  const [selected, setSelected] = useState(0);

  const handleSelect = () => {
    onSendMessage(QUICK_ACTIONS[selected].prompt);
  };

  return (
    <div className="flex flex-col gap-2 p-4">
      <div className="text-center text-xs text-gray-500 mb-1">
        🎮 Controller Mode — D-pad navigate, A to select, B to cancel
      </div>
      {QUICK_ACTIONS.map((action, i) => (
        <button
          key={action.id}
          onClick={() => { setSelected(i); handleSelect(); }}
          className={`text-left px-4 py-3 rounded-lg transition-colors text-sm ${
            i === selected
              ? 'bg-amber-600/60 text-white ring-2 ring-amber-400'
              : 'bg-white/10 text-gray-300 hover:bg-white/20'
          }`}
        >
          {action.label}
        </button>
      ))}
    </div>
  );
}
