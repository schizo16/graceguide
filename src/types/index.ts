export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export interface BuildStats {
  vigor: number;
  mind: number;
  endurance: number;
  strength: number;
  dexterity: number;
  intelligence: number;
  faith: number;
  arcane: number;
}

export interface BuildTemplate {
  name: string;
  starting_class: string;
  level: number;
  stats: BuildStats;
  weapons: string[];
  talismans: string[];
  armor: string[];
  playstyle: string;
  pros: string;
  cons: string;
  difficulty: string;
}
