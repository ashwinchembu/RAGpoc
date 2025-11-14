#!/usr/bin/env python3
"""
Load real documents from fetched_documents.json for use in the RAG notebook
"""

import json

def load_fetched_documents():
    """
    Load the documents fetched from public APIs
    """
    with open('fetched_documents.json', 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"✓ Loaded {len(documents)} documents from public sources")
    print("\nDocument sources breakdown:")
    
    sources = {}
    for doc in documents:
        source = doc.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sources.items():
        print(f"  - {source}: {count} documents")
    
    print("\nSample documents:")
    for i, doc in enumerate(documents[:5], 1):
        print(f"  {i}. {doc['title'][:60]}...")
    
    return documents


if __name__ == "__main__":
    docs = load_fetched_documents()
    print(f"\nTotal: {len(docs)} documents ready for RAG!")


