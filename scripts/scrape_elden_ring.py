"""One-time scraper and loader for Elden Ring data.
Outputs CSV files into backend/game_data/elden_ring/ and indexes into ChromaDB.

Usage: .venv/bin/python scripts/scrape_elden_ring.py [--index]
"""

import csv
import json
import os
import sys

OUTPUT_DIR = "backend/game_data/elden_ring"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Weapon data ────────────────────────────────────────────────────

WEAPONS = [
    {"id": 1, "name": "Longsword", "type": "straight_sword", "phys_dmg": 110, "str_req": 10, "dex_req": 10, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 3.0, "skill": "Square Off", "location": "Twin Maiden Husks"},
    {"id": 2, "name": "Broadsword", "type": "straight_sword", "phys_dmg": 125, "str_req": 10, "dex_req": 10, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 4.5, "skill": "Square Off", "location": "Stormveil Castle armory"},
    {"id": 3, "name": "Claymore", "type": "greatsword", "phys_dmg": 130, "str_req": 16, "dex_req": 13, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 9.0, "skill": "Stamp (Upward Cut)", "location": "Weeping Peninsula castle"},
    {"id": 4, "name": "Bloodhound's Fang", "type": "curved_greatsword", "phys_dmg": 141, "str_req": 18, "dex_req": 17, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "C", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 11.5, "skill": "Bloodhound's Finesse", "location": "Forlon Hound Evergaol (Limgrave)"},
    {"id": 5, "name": "Moonveil", "type": "katana", "phys_dmg": 99, "str_req": 12, "dex_req": 18, "int_req": 23, "fai_req": 0, "arc_req": 0, "str_scaling": "E", "dex_scaling": "D", "int_scaling": "C", "fai_scaling": "-", "arc_scaling": "-", "weight": 6.5, "skill": "Transient Moonlight", "location": "Gael Tunnel boss (Caelid)"},
    {"id": 6, "name": "Rivers of Blood", "type": "katana", "phys_dmg": 150, "str_req": 12, "dex_req": 18, "int_req": 0, "fai_req": 0, "arc_req": 20, "str_scaling": "E", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "D", "weight": 6.5, "skill": "Corpse Piler", "location": "Church of Repose (Mountaintops)"},
    {"id": 7, "name": "Dark Moon Greatsword", "type": "greatsword", "phys_dmg": 130, "str_req": 16, "dex_req": 11, "int_req": 38, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "E", "int_scaling": "C", "fai_scaling": "-", "arc_scaling": "-", "weight": 10.0, "skill": "Moonlight Greatsword", "location": "Ranni's quest reward"},
    {"id": 8, "name": "Blasphemous Blade", "type": "greatsword", "phys_dmg": 148, "str_req": 22, "dex_req": 15, "int_req": 0, "fai_req": 21, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "C", "arc_scaling": "-", "weight": 10.0, "skill": "Taker's Flames", "location": "Rykard remembrance"},
    {"id": 9, "name": "Sacred Relic Sword", "type": "greatsword", "phys_dmg": 113, "str_req": 14, "dex_req": 24, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "E", "arc_scaling": "-", "weight": 10.0, "skill": "Wave of Gold", "location": "Elden Beast remembrance"},
    {"id": 10, "name": "Giant-Crusher", "type": "colossal_weapon", "phys_dmg": 150, "str_req": 60, "dex_req": 0, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "A", "dex_scaling": "-", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 26.5, "skill": "Endure", "location": "Outer Wall Phantom Tree (carts)"},
    {"id": 11, "name": "Sword of Night and Flame", "type": "straight_sword", "phys_dmg": 87, "str_req": 13, "dex_req": 12, "int_req": 24, "fai_req": 24, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "B", "fai_scaling": "B", "arc_scaling": "-", "weight": 4.0, "skill": "Night-and-Flame Stance", "location": "Caria Manor"},
    {"id": 12, "name": "Uchigatana", "type": "katana", "phys_dmg": 103, "str_req": 11, "dex_req": 15, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 5.5, "skill": "Unsheathe", "location": "Deathtouched Catacombs"},
    {"id": 13, "name": "Nagakiba", "type": "katana", "phys_dmg": 123, "str_req": 18, "dex_req": 22, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "E", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 7.0, "skill": "Unsheathe", "location": "Yura questline"},
    {"id": 14, "name": "Starscourge Greatsword", "type": "colossal_weapon", "phys_dmg": 129, "str_req": 38, "dex_req": 15, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "C", "fai_scaling": "-", "arc_scaling": "-", "weight": 20.0, "skill": "Starcaller Cry", "location": "Radahn remembrance"},
    {"id": 15, "name": "Morgott's Cursed Sword", "type": "curved_greatsword", "phys_dmg": 148, "str_req": 14, "dex_req": 35, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "E", "dex_scaling": "C", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 9.0, "skill": "Cursed-Blood Slice", "location": "Morgott remembrance"},
    {"id": 16, "name": "Hand of Malenia", "type": "katana", "phys_dmg": 135, "str_req": 16, "dex_req": 48, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "E", "dex_scaling": "C", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 7.0, "skill": "Waterfowl Dance", "location": "Malenia remembrance"},
    {"id": 17, "name": "Bolt of Gransax", "type": "spear", "phys_dmg": 130, "str_req": 20, "dex_req": 40, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "E", "dex_scaling": "C", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 9.5, "skill": "Ancient Dragon's Lightning Strike", "location": "Leyndell capital"},
    {"id": 18, "name": "Winged Scythe", "type": "scythe", "phys_dmg": 120, "str_req": 16, "dex_req": 16, "int_req": 0, "fai_req": 24, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "C", "arc_scaling": "-", "weight": 5.5, "skill": "Angel's Wings", "location": "Tombsward Ruins (Weeping)"},
    {"id": 19, "name": "Godslayer's Greatsword", "type": "greatsword", "phys_dmg": 127, "str_req": 20, "dex_req": 22, "int_req": 0, "fai_req": 20, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "C", "arc_scaling": "-", "weight": 10.5, "skill": "The Queen's Black Flame", "location": "Godskin Apostle (Caelid Tower)"},
    {"id": 20, "name": "Guardian's Swordspear", "type": "halberd", "phys_dmg": 130, "str_req": 17, "dex_req": 16, "int_req": 0, "fai_req": 0, "arc_req": 0, "str_scaling": "D", "dex_scaling": "D", "int_scaling": "-", "fai_scaling": "-", "arc_scaling": "-", "weight": 9.0, "skill": "Impaling Thrust", "location": "Guardian enemies (Erdtrees)"},
]


def write_csv(filename, fieldnames, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--index":
        # Index into ChromaDB
        sys.path.insert(0, "backend")
        from game_data.loader import load_items_to_chroma
        load_items_to_chroma()
        print("Data indexed into ChromaDB")
    else:
        print("Scraping tool ready. Use --index to load into ChromaDB.")
        print(f"CSV files are in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
