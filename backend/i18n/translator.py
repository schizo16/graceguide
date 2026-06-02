"""Language detection and query translation.

Uses heuristics for MVP — no heavy model needed.
"""


def detect_language(text: str) -> str:
    """Simple heuristic: detect if text is Vietnamese by checking diacritics."""
    vietnamese_chars = set(
        "àáãạảăắằẳẵặâấầẩẫậđèéẹẻẽêềếểễệìíịỉĩ"
        "òóọỏõôốồổỗộơớờởỡợùúụủũưứừửữựỳýỵỷỹ"
    )
    # Count Vietnamese characters
    count = sum(1 for c in text.lower() if c in vietnamese_chars)
    # If >1% of text is Vietnamese diacritics, assume Vietnamese
    if len(text) > 0 and count / len(text) > 0.01:
        return "vi"
    return "en"


def translate_to_english(text: str, source_lang: str = "vi") -> str:
    """Return translation prompt instruction.
    
    Actual translation is done by the LLM via system prompt.
    This function just prepares metadata.
    """
    return text
