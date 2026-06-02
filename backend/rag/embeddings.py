"""Local embedding function using sentence-transformers."""

from sentence_transformers import SentenceTransformer

_MODEL = None


def get_embedding_function():
    """Lazy-load sentence transformer model (all-MiniLM-L6-v2)."""
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def embed_text(text: str) -> list[float]:
    """Embed a single text string into a 384-dim vector."""
    model = get_embedding_function()
    return model.encode(text).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Batch embed multiple texts."""
    model = get_embedding_function()
    return model.encode(texts).tolist()
