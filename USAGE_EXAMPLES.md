# Usage Examples - Azure RAG POC

This document provides practical examples of using the Azure RAG system.

## Basic Usage

### 1. Simple Question Answering

```python
# Ask a single question
result = rag_query("What is your return policy?")
display_answer(result)
```

**Output:**
```
================================================================================
QUESTION: What is your return policy?
================================================================================

ANSWER:
Based on our Product Returns Policy, customers can return items within 30 days 
of purchase. Items must be in their original condition with tags attached. 
Refunds are processed within 5-7 business days. For defective items, we offer 
immediate replacement at no additional cost. Please note that electronics must 
be returned within 14 days, and sale items are final sale unless defective.

────────────────────────────────────────────────────────────────────────────────
SOURCES USED (5 documents):
  1. Product Returns Policy
  2. Warranty Coverage
  3. Customer Support Hours
  4. Shipping Information
  5. Payment Methods
```

### 2. Adjusting Retrieval Parameters

```python
# Retrieve more documents for complex questions
result = rag_query(
    "What are all my options if a product is defective?",
    top_k=7,  # Retrieve 7 documents instead of 5
    temperature=0.5  # More focused answer
)
display_answer(result)
```

### 3. Batch Processing Questions

```python
# Process multiple questions
questions = [
    "What payment methods do you accept?",
    "How long does shipping take?",
    "Do you offer gift cards?",
    "What are your customer support hours?"
]

for question in questions:
    print(f"\n{'='*80}")
    print(f"Q: {question}")
    result = rag_query(question)
    print(f"A: {result['answer']}")
    print(f"Sources: {', '.join(result['sources'][:3])}")
```

## Advanced Usage

### 4. Custom Document Loading

#### Load from Directory

```python
import os
from glob import glob

# Load all documents from a directory
doc_dir = "my_documents"
file_paths = []

# Get all PDF, TXT, and MD files
file_paths.extend(glob(f"{doc_dir}/*.pdf"))
file_paths.extend(glob(f"{doc_dir}/*.txt"))
file_paths.extend(glob(f"{doc_dir}/*.md"))

# Load documents
my_documents = load_documents_from_files(file_paths)
print(f"Loaded {len(my_documents)} documents")
```

#### Load with Metadata

```python
# Add custom metadata to documents
documents = []
for file_path in file_paths:
    with open(file_path, 'r') as f:
        content = f.read()
    
    documents.append({
        'title': os.path.basename(file_path),
        'content': content,
        'source': file_path,
        'category': 'customer_service',  # Custom metadata
        'last_updated': '2024-01-15'
    })
```

### 5. Experiment with Chunking Strategies

```python
# Try different chunk sizes
chunk_sizes = [300, 500, 800]

for size in chunk_sizes:
    chunks = chunk_documents(sample_documents, chunk_size=size)
    print(f"Chunk size {size}: {len(chunks)} chunks created")
    
    # Compare retrieval quality
    # Smaller chunks = more precise but more chunks
    # Larger chunks = more context but less precise
```

### 6. Analyze Retrieval Quality

```python
# See which documents are being retrieved
question = "How do I return a defective product?"
result = rag_query(question)

print("\n📊 Retrieval Analysis:")
print(f"Question: {question}\n")

for i, doc in enumerate(result['retrieved_docs'], 1):
    print(f"{i}. {doc['document']['title']}")
    print(f"   Similarity: {doc['similarity']:.3f}")
    print(f"   Distance: {doc['distance']:.3f}")
    print(f"   Preview: {doc['document']['text'][:100]}...")
    print()
```

### 7. Compare Different Questions

```python
# Test semantic similarity
test_questions = [
    "What is your return policy?",
    "Can I get a refund?",
    "How do I send back an item?",
    "Return process explanation"
]

print("Testing semantic understanding:\n")
for question in test_questions:
    result = rag_query(question, top_k=3)
    print(f"Q: {question}")
    print(f"Top doc: {result['sources'][0]}")
    print(f"Similarity: {result['retrieved_docs'][0]['similarity']:.3f}\n")
```

### 8. Error Handling

```python
def safe_query(question: str, max_retries: int = 3) -> dict:
    """
    Query with retry logic for rate limits
    """
    for attempt in range(max_retries):
        try:
            return rag_query(question)
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Error: {e}")
                return {
                    'question': question,
                    'answer': "Sorry, I couldn't process your question.",
                    'sources': [],
                    'retrieved_docs': [],
                    'num_retrieved': 0
                }

# Use it
result = safe_query("What is your shipping policy?")
```

## Use Case Examples

### 9. Customer Service Bot

```python
class CustomerServiceBot:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.conversation_history = []
    
    def ask(self, question: str) -> str:
        """Ask a question and get an answer"""
        result = rag_query(question)
        
        # Store in history
        self.conversation_history.append({
            'question': question,
            'answer': result['answer'],
            'sources': result['sources']
        })
        
        return result['answer']
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history

# Usage
bot = CustomerServiceBot(vector_store)

print("Bot:", bot.ask("What payment methods do you accept?"))
print("\nBot:", bot.ask("Do you accept PayPal?"))
print("\nBot:", bot.ask("What about international orders?"))

# Review conversation
for i, exchange in enumerate(bot.get_history(), 1):
    print(f"\n--- Exchange {i} ---")
    print(f"User: {exchange['question']}")
    print(f"Bot: {exchange['answer'][:100]}...")
```

### 10. Document Search Interface

```python
def search_documents(query: str, show_context: bool = True):
    """
    Search documents and show results
    """
    # Get embedding for query
    query_embedding = get_embeddings([query])[0]
    
    # Search
    results = vector_store.search(query_embedding, k=10)
    
    print(f"\n🔍 Search Results for: '{query}'")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"\n{i}. {doc['title']}")
        print(f"   Similarity: {result['similarity']:.3f}")
        
        if show_context:
            print(f"   Context: {doc['text'][:150]}...")
    
    return results

# Usage
search_results = search_documents("refund process")
```

### 11. FAQ Generator

```python
def generate_faq(questions: list) -> dict:
    """
    Generate FAQ from list of questions
    """
    faq = {}
    
    print("Generating FAQ...")
    for question in questions:
        result = rag_query(question, temperature=0.3)  # Lower temp for consistency
        faq[question] = {
            'answer': result['answer'],
            'sources': result['sources']
        }
        print(f"✓ {question}")
    
    return faq

# Usage
common_questions = [
    "What is your return policy?",
    "How long does shipping take?",
    "What payment methods do you accept?",
    "How can I track my order?",
    "Do you offer international shipping?"
]

faq = generate_faq(common_questions)

# Export to markdown
with open('faq_output.md', 'w') as f:
    f.write("# Frequently Asked Questions\n\n")
    for question, data in faq.items():
        f.write(f"## {question}\n\n")
        f.write(f"{data['answer']}\n\n")
        f.write(f"*Sources: {', '.join(data['sources'][:3])}*\n\n")

print("FAQ saved to faq_output.md")
```

### 12. Document Quality Analysis

```python
def analyze_document_coverage():
    """
    Analyze which documents are being used most
    """
    test_questions = [
        "return policy", "shipping cost", "payment methods",
        "customer support", "warranty", "tracking order",
        "bulk discounts", "gift cards", "loyalty program"
    ]
    
    doc_usage = {}
    
    for question in test_questions:
        result = rag_query(question)
        for source in result['sources']:
            doc_usage[source] = doc_usage.get(source, 0) + 1
    
    # Sort by usage
    sorted_docs = sorted(doc_usage.items(), key=lambda x: x[1], reverse=True)
    
    print("\n📈 Document Usage Analysis")
    print("="*60)
    for doc, count in sorted_docs:
        bar = "█" * count
        print(f"{doc:30} {bar} ({count})")
    
    # Identify unused documents
    all_docs = set(doc['title'] for doc in sample_documents)
    used_docs = set(doc_usage.keys())
    unused = all_docs - used_docs
    
    if unused:
        print(f"\n⚠️  Unused documents: {unused}")
        print("Consider reviewing these documents or adding more diverse questions.")

# Run analysis
analyze_document_coverage()
```

### 13. Multi-language Support (if needed)

```python
def translate_and_query(question: str, target_lang: str = 'en'):
    """
    Translate question and answer (requires translation service)
    """
    # This is a placeholder - you'd integrate with Azure Translator
    # or another translation service
    
    # For English documents, query directly
    result = rag_query(question)
    
    # Add note about translation if needed
    if target_lang != 'en':
        result['note'] = f"Answer translated to {target_lang}"
    
    return result
```

### 14. Confidence Scoring

```python
def query_with_confidence(question: str, confidence_threshold: float = 0.7):
    """
    Query and include confidence score
    """
    result = rag_query(question)
    
    # Calculate confidence based on top document similarity
    top_similarity = result['retrieved_docs'][0]['similarity']
    
    result['confidence'] = top_similarity
    result['confident'] = top_similarity >= confidence_threshold
    
    if not result['confident']:
        result['answer'] += "\n\n⚠️ Note: I found limited information about this question. Please contact support for more details."
    
    return result

# Usage
result = query_with_confidence("What is your return policy?")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Answer: {result['answer']}")
```

## Performance Testing

### 15. Benchmark System Performance

```python
import time

def benchmark():
    """
    Test system performance
    """
    test_questions = [
        "What is your return policy?",
        "How much does shipping cost?",
        "What payment methods do you accept?",
        "Do you offer bulk discounts?",
        "How can I contact customer support?"
    ]
    
    results = []
    
    print("Running benchmark...")
    print("="*60)
    
    for question in test_questions:
        start = time.time()
        result = rag_query(question)
        elapsed = time.time() - start
        
        results.append({
            'question': question,
            'time': elapsed,
            'answer_length': len(result['answer']),
            'num_sources': len(result['sources'])
        })
        
        print(f"✓ {question[:40]:40} {elapsed:.2f}s")
    
    # Summary
    avg_time = sum(r['time'] for r in results) / len(results)
    print(f"\n📊 Average response time: {avg_time:.2f}s")
    print(f"   Fastest: {min(r['time'] for r in results):.2f}s")
    print(f"   Slowest: {max(r['time'] for r in results):.2f}s")

# Run benchmark
benchmark()
```

## Tips and Best Practices

1. **Question Formulation**: More specific questions get better answers
   - ❌ "shipping"
   - ✅ "How long does standard shipping take?"

2. **Temperature Settings**:
   - 0.3-0.5: Factual Q&A, consistent answers
   - 0.7-0.8: More natural, conversational
   - 0.9-1.0: Creative, varied (less suitable for factual Q&A)

3. **Top-K Selection**:
   - Start with 5
   - Increase for complex questions
   - Decrease for simpler questions or to reduce cost

4. **Document Quality**:
   - Well-structured documents retrieve better
   - Clear headings help chunking
   - Remove irrelevant boilerplate

5. **Monitoring**:
   - Log all queries and responses
   - Track confidence scores
   - Identify common questions for caching

## Next Steps

- Try these examples with your own documents
- Adjust parameters based on your use case
- Build custom applications using the RAG pipeline
- Monitor and optimize for your specific needs

