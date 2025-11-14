# Quick Start Guide - Azure RAG POC

Get up and running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
cd /Users/ashwin/zs/RAGpoc
pip install -r requirements.txt
```

## Step 2: Configure Azure OpenAI (1 minute)

1. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Azure credentials:
   ```env
   AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
   AZURE_OPENAI_API_KEY=YOUR-KEY-HERE
   AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   AZURE_CHAT_DEPLOYMENT=gpt-4
   ```

### Where to Find Your Azure Credentials

1. **Endpoint**: Azure Portal → Your OpenAI Resource → "Keys and Endpoint" section
2. **API Key**: Same location, copy either Key 1 or Key 2
3. **Deployment Names**: Azure OpenAI Studio → Deployments → Copy the deployment names

## Step 3: Run the Notebook (2 minutes)

```bash
jupyter lab azure_rag_poc.ipynb
```

Or if you prefer Jupyter Notebook:
```bash
jupyter notebook azure_rag_poc.ipynb
```

## Step 4: Test It Out!

1. Run all cells (Cell → Run All)
2. Wait for embeddings to generate (~30 seconds)
3. See results from the test questions
4. Try the interactive Q&A (optional)

## Example Questions to Try

```python
result = rag_query("What is your return policy?")
display_answer(result)
```

```python
result = rag_query("How can I track my order?")
display_answer(result)
```

```python
result = rag_query("What payment methods are available?")
display_answer(result)
```

## Using Your Own Documents

Replace the sample documents with your own:

```python
# Load your 30 documents
my_files = [
    'path/to/doc1.pdf',
    'path/to/doc2.txt',
    'path/to/doc3.md',
    # ... add all your documents
]

my_documents = load_documents_from_files(my_files)
my_chunks = chunk_documents(my_documents)
chunk_texts = [chunk['text'] for chunk in my_chunks]
my_embeddings = get_embeddings(chunk_texts)
my_vector_store = VectorStore(my_embeddings, my_chunks)
```

## Troubleshooting

**Problem**: "Authentication failed"  
**Solution**: Double-check your API key and endpoint in `.env`

**Problem**: "Model not found"  
**Solution**: Verify deployment names match exactly (case-sensitive)

**Problem**: "Rate limit exceeded"  
**Solution**: Wait a few seconds and try again

## What's Next?

- ✅ Test with sample documents
- ✅ Load your actual 30 documents
- ✅ Fine-tune chunk size and retrieval parameters
- ✅ Export to production API (see README.md)

## Need Help?

Refer to the full [README.md](README.md) for detailed documentation.

