"""Chat service: handles RAG + LLM flow."""

import ollama
from rag.retriever import retrieve
from chat.prompts import get_system_prompt

OLLAMA_MODEL = "llama3.1:8b"


def generate_response(user_message: str, language: str = "en") -> str:
    """Full RAG pipeline: retrieve context -> call LLM -> return response."""
    # 1. Retrieve relevant game knowledge
    context_docs = retrieve(user_message, k=5)
    context = "\n\n".join([d["text"] for d in context_docs])

    # 2. Build prompt with context
    system_prompt = get_system_prompt(language)
    user_prompt = f"""Context from Elden Ring database:
{context}

User question: {user_message}

Answer concisely based on the context above. If the context doesn't contain relevant info, say so."""

    # 3. Call local LLM via Ollama
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": 0.7, "num_predict": 512},
        )
        return response["message"]["content"]
    except Exception as e:
        return f"⚠️ AI Error: {e}\n\nMake sure Ollama is running and the model '{OLLAMA_MODEL}' is pulled."
