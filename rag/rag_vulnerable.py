"""
Lab 2 - Vulnerable RAG (provided complete, NO defenses).

Retrieves from a knowledge base that contains a poisoned document and feeds
every retrieved chunk straight to the LLM. Run it, then ask the questions in
the lab to watch the poisoned content reach the answer.
"""
from kb import load_chunks, retrieve, rag_answer


def main():
    chunks = load_chunks()
    sources = sorted({c["source"] for c in chunks})
    print("=== VULNERABLE RAG (no security) ===")
    print(f"Knowledge base loaded: {len(chunks)} chunks from {len(sources)} sources")
    for s in sources:
        print(f"  - {s}")
    print("\nType a question (or 'quit').")

    while True:
        try:
            q = input("\n> ").strip()
        except EOFError:
            break
        if q.lower() in ("quit", "exit"):
            break
        if not q:
            continue
        hits = retrieve(q, chunks, k=3)
        print("\nSOURCES:")
        for h in hits:
            print(f"  [{h['relevance']}] {h['source']}")
        print("\nANSWER:")
        print(rag_answer(q, hits))


if __name__ == "__main__":
    main()
