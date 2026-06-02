"""ChromaDB vector store wrapper."""

import chromadb
from chromadb.config import Settings

_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path="backend/elden-ring/chroma",
            settings=Settings(anonymized_telemetry=False),
        )
    return _client


def get_collection(name: str = "elden_ring"):
    """Get or create a collection."""
    client = get_client()
    try:
        return client.get_collection(name)
    except ValueError:
        return client.create_collection(name)
