# Simple in-memory storage for Phase 1
DOCUMENT_CONTEXT = ""

def set_document_context(text: str):
    global DOCUMENT_CONTEXT
    DOCUMENT_CONTEXT = text

def process_query(query: str, strategy: str = "auto") -> str:
    # Phase 1: Context Window Only
    if not DOCUMENT_CONTEXT:
        return "Please upload a document first."
    
    # Mock LLM interaction for now
    # In real implementation this would call OpenAI/Gemini/Anthropic
    prompt = f"Context:\n{DOCUMENT_CONTEXT}\n\nQuestion: {query}\n\nAnswer:"
    
    return f"[Mock Response] Based on the document (length {len(DOCUMENT_CONTEXT)} chars), here is the answer to '{query}'..."
