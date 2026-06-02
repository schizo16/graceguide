import { useState } from 'react';

interface Props {
  onComplete: (buildName: string) => void;
}

const STEPS = [
  {
    question: 'Your preferred playstyle?',
    subtitle: 'Choose how you like to fight',
    options: [
      { id: 'strength', emoji: '⚔️', label: 'Strength', desc: 'Slow but heavy damage, stagger enemies' },
      { id: 'dexterity', emoji: '🗡️', label: 'Dexterity', desc: 'Fast attacks, crits, dodging' },
      { id: 'intelligence', emoji: '🔮', label: 'Intelligence', desc: 'Ranged magic, big spells' },
      { id: 'faith', emoji: '✨', label: 'Faith', desc: 'Buffs, healing, holy/fire damage' },
      { id: 'arcane', emoji: '🩸', label: 'Arcane', desc: 'Bleed, poison, status effects' },
      { id: 'unknown', emoji: '🤷', label: 'Not sure', desc: "I'm new, recommend me something" },
    ],
  },
  {
    question: 'Preferred difficulty?',
    subtitle: 'How hard do you want it?',
    options: [
      { id: 'easy', emoji: '🛡️', label: 'Easy', desc: 'Tanky, forgiving, beginner-friendly' },
      { id: 'medium', emoji: '⚖️', label: 'Balanced', desc: 'Mix of survival and damage' },
      { id: 'hard', emoji: '💀', label: 'Hardcore', desc: 'Glass cannon, maximum DPS' },
    ],
  },
  {
    question: 'Favorite weapon type?',
    subtitle: 'What feels right in your hands?',
    options: [
      { id: 'greatsword', emoji: '🗡️', label: 'Greatswords', desc: 'Big, heavy, satisfying' },
      { id: 'katana', emoji: '⚔️', label: 'Katanas', desc: 'Fast, bleed, elegant' },
      { id: 'hammer', emoji: '🔨', label: 'Hammers', desc: 'Stagger, crush armor' },
      { id: 'spear', emoji: '🔱', label: 'Spears', desc: 'Safe range, poking' },
      { id: 'staff', emoji: '🪄', label: 'Staff / Seal', desc: 'Casting magic' },
      { id: 'unknown', emoji: '🤷', label: 'Any', desc: 'Surprise me' },
    ],
  },
];

export default function OnboardingFlow({ onComplete }: Props) {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);

  const handleSelect = async (optionId: string) => {
    const newAnswers = [...answers, optionId];
    if (step < STEPS.length - 1) {
      setAnswers(newAnswers);
      setStep(step + 1);
    } else {
      // Complete onboarding
      try {
        const resp = await fetch('http://127.0.0.1:3721/onboarding/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            playstyle: newAnswers[0],
            difficulty: newAnswers[1],
            weapon_pref: newAnswers[2],
          }),
        });
        const data = await resp.json();
        onComplete(data.build?.name || 'Recommended Build');
      } catch {
        // Fallback if backend not running
        onComplete('Quality Beginner Build');
      }
    }
  };

  const current = STEPS[step];

  return (
    <div className="flex flex-col items-center justify-center h-full p-6 bg-gradient-to-b from-gray-900 to-black">
      <h1 className="text-2xl font-bold text-amber-400 mb-1">🎮 GraceGuide</h1>
      <p className="text-gray-500 text-sm mb-8">Let's find your perfect build</p>

      {/* Progress dots */}
      <div className="flex gap-1 mb-6">
        {STEPS.map((_, i) => (
          <div
            key={i}
            className={`h-1 w-8 rounded-full transition-colors ${
              i <= step ? 'bg-amber-500' : 'bg-gray-800'
            }`}
          />
        ))}
      </div>

      <h2 className="text-lg font-semibold text-white mb-1">{current.question}</h2>
      <p className="text-xs text-gray-600 mb-5">{current.subtitle}</p>

      <div className="w-full max-w-sm space-y-2">
        {current.options.map((opt) => (
          <button
            key={opt.id}
            onClick={() => handleSelect(opt.id)}
            className="w-full text-left px-4 py-3 bg-white/5 hover:bg-white/10
                       rounded-lg transition-colors border border-white/5
                       hover:border-amber-600/30"
          >
            <span className="text-white text-sm">
              {opt.emoji} {opt.label}
            </span>
            <p className="text-gray-600 text-[11px] mt-0.5">{opt.desc}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
