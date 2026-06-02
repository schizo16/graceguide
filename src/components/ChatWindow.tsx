import { useState } from 'react';
import { useOverlay } from '../hooks/useOverlay';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ControllerMode from './ControllerMode';

export default function ChatWindow() {
  const { messages, isStreaming, sendMessage } = useOverlay();
  const [controllerMode] = useState(false);

  return (
    <div className="flex flex-col h-full">
      {/* Header - draggable region */}
      <div
        className="flex items-center justify-between px-4 py-2 bg-black/40 shrink-0"
        data-tauri-drag-region
      >
        <div className="flex items-center gap-2">
          <span className="text-amber-400 font-bold text-sm">GraceGuide</span>
          <span className="text-xs text-gray-600">|</span>
          <span className="text-xs text-green-400/70">Elden Ring</span>
        </div>
        <div className="flex gap-2 text-gray-500 text-xs">
          <button className="hover:text-white transition-colors" title="Settings">
            ⚙
          </button>
          <button className="hover:text-white transition-colors" title="Language">
            EN
          </button>
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-3">
        {messages.length === 0 && !controllerMode && (
          <div className="text-gray-600 text-sm text-center mt-12">
            <p className="text-xl mb-2 text-gray-500">🎮 GraceGuide</p>
            <p>Ask me about builds, bosses, items, or lore...</p>
            <p className="text-xs mt-4 text-gray-700">
              Ctrl+Alt+G to toggle · Esc to hide
            </p>
          </div>
        )}
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isStreaming && (
          <div className="flex items-center gap-2 text-gray-500 text-xs animate-pulse">
            <span className="w-2 h-2 bg-amber-500 rounded-full" />
            AI is thinking...
          </div>
        )}
      </div>

      {/* Controller mode or chat input */}
      {controllerMode ? (
        <ControllerMode onSendMessage={sendMessage} />
      ) : (
        <ChatInput onSend={sendMessage} disabled={isStreaming} />
      )}
    </div>
  );
}
