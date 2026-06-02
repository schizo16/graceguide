"""Build recommender — decision tree based on 3 questions."""

import json
import os

BUILDS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "game_data", "elden_ring", "builds.json"
)

_PLAYSTYLE_MAP = {
    "strength": "Unga Bunga Strength",
    "dexterity": "Quality Beginner Build",
    "intelligence": "Dex/Int Mage Knight",
    "faith": "Pure Faith Paladin",
    "arcane": "Arcane Bleed Build",
    "unknown": "Quality Beginner Build",
}


def load_builds() -> list[dict]:
    if not os.path.exists(BUILDS_PATH):
        return _default_builds()
    with open(BUILDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _default_builds() -> list[dict]:
    """Fallback builds if JSON file is missing."""
    return [
        {
            "name": "Quality Beginner Build",
            "starting_class": "Vagabond",
            "level": 80,
            "stats": {
                "vigor": 40, "mind": 10, "endurance": 25,
                "strength": 20, "dexterity": 20, "intelligence": 9,
                "faith": 9, "arcane": 7,
            },
            "weapons": ["Bloodhound's Fang", "Claymore"],
            "talismans": ["Green Turtle Talisman", "Erdtree's Favor"],
            "armor": ["Knight Set"],
            "playstyle": "Jack of all trades, try everything",
            "pros": "Flexible, try all weapons, great for new players",
            "cons": "Not optimal at high levels",
            "difficulty": "easy",
        }
    ]


def recommend(
    playstyle: str, difficulty: str, weapon_pref: str | None = None
) -> dict:
    """Recommend a build based on user preferences."""
    builds = load_builds()
    build_name = _PLAYSTYLE_MAP.get(playstyle, "Quality Beginner Build")
    for build in builds:
        if build["name"] == build_name:
            return build
    return builds[0]


def get_build_summary(build: dict) -> str:
    """Format build as a readable summary."""
    stats = build["stats"]
    return (
        f"📦 BUILD: {build['name']} (Level {build['level']})\n"
        f"────────────────────────────────\n"
        f"Playstyle: {build['playstyle']}\n"
        f"Difficulty: {build['difficulty']}\n\n"
        f"Stats:\n"
        f"  Vigor: {stats['vigor']}  |  Mind: {stats['mind']}  |  "
        f"Endurance: {stats['endurance']}\n"
        f"  Strength: {stats['strength']}  |  Dexterity: {stats['dexterity']}\n"
        f"  Intelligence: {stats['intelligence']}  |  "
        f"Faith: {stats['faith']}  |  Arcane: {stats['arcane']}\n\n"
        f"Weapons: {', '.join(build['weapons'])}\n"
        f"Talismans: {', '.join(build['talismans'])}\n"
        f"Armor: {', '.join(build['armor'])}\n\n"
        f"Pros: {build['pros']}\n"
        f"Cons: {build['cons']}"
    )
