import { Message } from '../types';
import BuildCard from './BuildCard';

interface Props {
  message: Message;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === 'user';
  const hasBuildData = message.content.includes('BUILD') || message.content.includes('Stats:');

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
          isUser
            ? 'bg-amber-600/20 text-amber-100'
            : 'bg-white/10 text-gray-200'
        }`}
      >
        <p className="whitespace-pre-wrap break-words">{message.content}</p>
        {hasBuildData && <BuildCard />}
        <p className="text-[10px] text-gray-600 mt-1">
          {new Date(message.timestamp).toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
}
