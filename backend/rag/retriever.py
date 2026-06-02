"""RAG retrieval: query → embed → search."""

from rag.embeddings import embed_text
from rag.vector_store import get_collection


def retrieve(query: str, k: int = 10) -> list[dict]:
    """Search ChromaDB for relevant chunks."""
    collection = get_collection()
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    documents = []
    for i in range(len(results["ids"][0])):
        documents.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": results["distances"][0][i] if results.get("distances") else 0,
        })
    return documents
