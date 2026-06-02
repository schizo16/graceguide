import { useState, useCallback, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import type { Message } from '../types';

export function useOverlay() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentGame, setCurrentGame] = useState<string | null>(null);

  useEffect(() => {
    // Poll game status every 5s
    const interval = setInterval(async () => {
      try {
        const resp = await fetch('http://127.0.0.1:3721/game/current');
        const data = await resp.json();
        setCurrentGame(data.game);
      } catch {
        // Backend not available
      }
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = useCallback(async (text: string) => {
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsStreaming(true);

    try {
      const response = await invoke<string>('chat', { message: text });
      const aiMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content:
          '⚠️ AI is not available. Make sure Ollama is running.\n\nTry: `ollama pull llama3.1:8b`',
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    }
    setIsStreaming(false);
  }, []);

  return { messages, isStreaming, currentGame, sendMessage, setMessages };
}
