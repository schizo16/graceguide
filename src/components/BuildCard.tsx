interface Props {
  build?: {
    name: string;
    level: number;
    stats: Record<string, number>;
    weapons: string[];
    talismans: string[];
  };
}

export default function BuildCard({ build }: Props) {
  // If no build provided, show static example
  const stats = build?.stats || {
    Vigor: 40, Mind: 10, Endurance: 25,
    Strength: 20, Dexterity: 20, Intelligence: 9,
    Faith: 9, Arcane: 7,
  };

  const maxStat = Math.max(...Object.values(stats), 60);

  return (
    <div className="mt-2 bg-gray-800/80 rounded-lg p-3 border border-amber-600/30">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-lg">📦</span>
        <span className="font-bold text-amber-300 text-xs uppercase tracking-wide">
          {build?.name || 'Recommended Build'}
        </span>
        {build?.level && (
          <span className="text-xs text-gray-500">Lv.{build.level}</span>
        )}
      </div>

      {/* Stat bars */}
      <div className="space-y-1">
        {Object.entries(stats).map(([name, value]) => (
          <div key={name} className="flex items-center gap-2 text-xs">
            <span className="w-16 text-gray-400 text-right">{name}</span>
            <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-amber-600/60 rounded-full transition-all"
                style={{ width: `${(value / maxStat) * 100}%` }}
              />
            </div>
            <span className="w-6 text-gray-300">{value}</span>
          </div>
        ))}
      </div>

      {/* Weapons / Talismans */}
      {build?.weapons && (
        <div className="mt-2 text-xs text-gray-400">
          <span className="text-amber-400">Weapons:</span>{' '}
          {build.weapons.join(', ')}
        </div>
      )}
      {build?.talismans && (
        <div className="text-xs text-gray-400">
          <span className="text-amber-400">Talismans:</span>{' '}
          {build.talismans.join(', ')}
        </div>
      )}
    </div>
  );
}
