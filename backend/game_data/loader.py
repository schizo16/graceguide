"""Load CSV data into ChromaDB vector store.
Run: .venv/bin/python -c "from game_data.loader import load_items_to_chroma; load_items_to_chroma()"
"""

import csv
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "elden_ring")


def load_items_to_chroma():
    """Read all CSVs and index into ChromaDB."""
    from rag.vector_store import get_collection

    collection = get_collection("elden_ring")

    # Clear existing data
    try:
        collection.delete(collection.get()["ids"])
    except Exception:
        pass

    documents = []
    metadatas = []
    ids = []

    # Load bosses
    bosses_path = os.path.join(DATA_DIR, "bosses.csv")
    if os.path.exists(bosses_path):
        with open(bosses_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = (
                    f"Boss: {row['name']}. Area: {row['area']}. "
                    f"Health: {row['health']}. Weaknesses: {row['weaknesses']}. "
                    f"Resistances: {row['resistances']}. Drops: {row['drops']}. "
                    f"Phases: {row['phases']}. Walkthrough: {row['walkthrough']}"
                )
                documents.append(doc)
                metadatas.append({
                    "type": "boss",
                    "name": row["name"],
                    "area": row["area"],
                })
                ids.append(f"boss_{row['id']}")

    # Load weapons
    weapons_path = os.path.join(DATA_DIR, "weapons.csv")
    if os.path.exists(weapons_path):
        with open(weapons_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = (
                    f"Weapon: {row['name']}. Type: {row['type']}. "
                    f"Physical Damage: {row['phys_dmg']}. "
                    f"Requirements: STR {row['str_req']}, DEX {row['dex_req']}, "
                    f"INT {row['int_req']}, FAI {row['fai_req']}, ARC {row['arc_req']}. "
                    f"Scaling: STR {row['str_scaling']}, DEX {row['dex_scaling']}. "
                    f"Weight: {row['weight']}. Skill: {row['skill']}. "
                    f"Location: {row['location']}"
                )
                documents.append(doc)
                metadatas.append({
                    "type": "weapon",
                    "name": row["name"],
                    "category": row.get("type", ""),
                })
                ids.append(f"weapon_{row['id']}")

    # Load areas
    areas_path = os.path.join(DATA_DIR, "areas.csv")
    if os.path.exists(areas_path):
        with open(areas_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = (
                    f"Area: {row['name']}. Area: {row['area']}. "
                    f"Description: {row['description']}. "
                    f"Recommended Level: {row['recommended_level']}. "
                    f"Bosses: {row['bosses']}. Items: {row['items']}"
                )
                documents.append(doc)
                metadatas.append({
                    "type": "area",
                    "name": row["name"],
                    "area": row.get("area", ""),
                })
                ids.append(f"area_{row['id']}")

    if not documents:
        print("No data found. Run scrape script first.")
        return

    # Index in batches of 100
    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch_end = min(i + batch_size, len(documents))
        collection.add(
            documents=documents[i:batch_end],
            metadatas=metadatas[i:batch_end],
            ids=ids[i:batch_end],
        )
        print(f"Indexed {batch_end}/{len(documents)} items...")

    print(f"✅ Done! Indexed {len(documents)} items into ChromaDB collection 'elden_ring'")
