# RAG Architecture Documentation

## What is RAG?

**Retrieval Augmented Generation (RAG)** is a technique that combines:
1. **Information Retrieval** - Finding relevant documents
2. **Language Generation** - Using LLM to create answers

This approach gives you:
- ✅ Accurate answers grounded in your documents
- ✅ Source citations for transparency
- ✅ Up-to-date information (just update docs)
- ✅ Cost-effective (only send relevant context to LLM)

## System Architecture

### High-Level Flow

```
User Question
     │
     ▼
┌─────────────────────────────────────┐
│  1. Question Embedding Generation   │
│     (Azure OpenAI)                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. Vector Similarity Search        │
│     (FAISS)                         │
│     - Find top-k most similar docs  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. Context Preparation             │
│     - Combine retrieved documents   │
│     - Format with metadata          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. LLM Answer Generation           │
│     (Azure OpenAI GPT-4)            │
│     - Answer based on context       │
│     - Cite sources                  │
└──────────────┬──────────────────────┘
               │
               ▼
    Answer + Sources
```

### Component Details

#### 1. Document Processing Pipeline

```
Raw Documents (PDF, TXT, MD)
         │
         ▼
    Text Extraction
         │
         ▼
    Text Chunking
    (500 chars, 50 overlap)
         │
         ▼
    Embedding Generation
    (Azure OpenAI)
         │
         ▼
    Vector Storage
    (FAISS Index)
```

**Why chunking?**
- Embeddings have token limits
- Smaller chunks = more precise retrieval
- Overlap ensures context isn't lost at boundaries

#### 2. Embedding Model

**Model**: `text-embedding-ada-002` (Azure OpenAI)
- **Dimension**: 1536
- **Max tokens**: 8191
- **Cost**: $0.0001 per 1K tokens
- **Performance**: State-of-the-art retrieval accuracy

#### 3. Vector Store (FAISS)

**FAISS** (Facebook AI Similarity Search)
- In-memory vector database
- L2 (Euclidean) distance metric
- Sub-millisecond search for thousands of vectors
- No external dependencies (great for POC)

**For Production**: Consider Azure AI Search
- Managed service
- Hybrid search (vector + keyword)
- Filtering and faceting
- Security and compliance

#### 4. LLM (GPT-4)

**Model**: `gpt-4` or `gpt-35-turbo`
- **Context window**: 8K tokens (gpt-4), 4K (gpt-35-turbo)
- **Temperature**: 0.7 (balanced creativity/accuracy)
- **Max tokens**: 500 (for concise answers)

## Data Flow Example

### Example: "What is your return policy?"

```
1. QUESTION EMBEDDING
   Input: "What is your return policy?"
   Output: [0.012, -0.034, 0.056, ...] (1536 dims)

2. VECTOR SEARCH
   Query vector against document embeddings
   Top 5 matches:
   - Product Returns Policy (similarity: 0.89)
   - Warranty Coverage (similarity: 0.72)
   - Customer Support Hours (similarity: 0.65)
   - Shipping Information (similarity: 0.61)
   - Account Security (similarity: 0.58)

3. CONTEXT ASSEMBLY
   Document: Product Returns Policy
   Our product returns policy allows customers to return items 
   within 30 days of purchase. Items must be in original 
   condition with tags attached...
   
   Document: Warranty Coverage
   All products come with a 1-year manufacturer warranty...
   
   [... top 5 documents]

4. LLM PROMPT
   System: You are a helpful customer service assistant...
   User: Context documents:
         [assembled context]
         
         Question: What is your return policy?

5. LLM RESPONSE
   "Based on our Product Returns Policy, customers can return 
   items within 30 days of purchase. Items must be in their 
   original condition with tags attached. Refunds are processed 
   within 5-7 business days. For electronics, the return window 
   is 14 days. If an item is defective, we offer immediate 
   replacement at no additional cost."

6. FINAL OUTPUT
   Answer: [LLM response]
   Sources: ["Product Returns Policy", "Warranty Coverage", ...]
   Retrieved: 5 documents
```

## Key Parameters and Tuning

### Chunk Size (500 chars)
- **Too small**: Loss of context, more chunks to manage
- **Too large**: Less precise retrieval, token limit issues
- **Optimal**: 300-800 characters for typical docs

### Chunk Overlap (50 chars)
- Prevents information loss at chunk boundaries
- Typical: 10-20% of chunk size

### Top-K Retrieval (5 docs)
- **Too few**: Might miss relevant info
- **Too many**: Context pollution, higher cost
- **Optimal**: 3-7 for most use cases

### Temperature (0.7)
- **0.0**: Deterministic, focused
- **1.0**: Creative, varied
- **0.5-0.8**: Good for Q&A

### Max Tokens (500)
- Balance between completeness and cost
- Adjust based on expected answer length

## Advantages of This Architecture

### 1. Accuracy
- Answers grounded in your documents
- No hallucination (if docs don't have info, it says so)
- Source citations for verification

### 2. Cost-Effective
- Only relevant context sent to LLM
- Embedding once, query many times
- Much cheaper than fine-tuning

### 3. Maintainable
- Easy to update knowledge (just re-embed changed docs)
- No model retraining needed
- Version control for documents

### 4. Scalable
- Handles thousands of documents
- Sub-second retrieval
- Can scale to millions with proper vector DB

### 5. Transparent
- See which documents were used
- Debug retrieval quality
- User trust through citations

## Limitations and Considerations

### 1. Retrieval Quality
- Depends on embedding model quality
- May miss relevant docs if not semantically similar
- No reasoning across multiple unrelated docs

### 2. Context Window
- LLM has token limits
- Can't send all documents
- May need multiple queries for complex questions

### 3. Update Lag
- New documents need re-embedding
- Not real-time (but can be near real-time)

### 4. Query Formulation
- Quality depends on how question is asked
- May need query expansion/reformulation

## Production Enhancements

### 1. Hybrid Search
Combine vector search with keyword search:
```python
# Vector score: 0.8
# Keyword score: 0.6
# Final score: 0.8 * 0.7 + 0.6 * 0.3 = 0.74
```

### 2. Re-ranking
- Use cross-encoder to re-rank retrieved docs
- More accurate but slower
- Apply to top-k candidates

### 3. Query Expansion
- Generate variations of user query
- Search with all variations
- Combine results

### 4. Metadata Filtering
```python
# Only search in specific document categories
filter = {"category": "returns", "date": "> 2023"}
results = vector_store.search(query, filter=filter)
```

### 5. Caching
- Cache frequent queries
- Reduce latency and cost
- Redis or in-memory cache

### 6. Monitoring
- Track retrieval quality
- Log failed queries
- A/B test parameters

## Comparison with Alternatives

### vs. Fine-tuning
| Aspect | RAG | Fine-tuning |
|--------|-----|-------------|
| Cost | Low | High |
| Update Speed | Minutes | Hours/Days |
| Data Required | Minimal | Large dataset |
| Transparency | High (citations) | Low (black box) |
| Use Case | Knowledge base | Task-specific |

### vs. Long Context Models
| Aspect | RAG | Long Context |
|--------|-----|-------------|
| Cost per query | Low | High |
| Scalability | Excellent | Limited |
| Relevance | High (retrieval) | Lower (all context) |
| Max documents | Unlimited | ~10-50 |

## References and Resources

- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- [Retrieval-Augmented Generation Paper](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)

