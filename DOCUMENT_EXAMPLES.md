# Document Loading Examples

This guide shows how to prepare and load your 30 documents for the RAG system.

## Supported Formats

✅ Text files (.txt)  
✅ PDF files (.pdf)  
✅ Markdown files (.md)  
✅ Any text-based format (with minor code changes)

## Document Organization

### Recommended Structure

```
RAGpoc/
├── documents/
│   ├── returns_policy.pdf
│   ├── shipping_info.txt
│   ├── warranty.md
│   ├── payment_methods.pdf
│   └── ... (26 more documents)
├── azure_rag_poc.ipynb
└── ... (other files)
```

## Example: Loading Your Documents

### Option 1: From a Directory

```python
import os
from glob import glob

# Point to your documents directory
doc_directory = "documents"

# Load all supported file types
file_paths = []
file_paths.extend(glob(f"{doc_directory}/*.pdf"))
file_paths.extend(glob(f"{doc_directory}/*.txt"))
file_paths.extend(glob(f"{doc_directory}/*.md"))

print(f"Found {len(file_paths)} documents:")
for path in file_paths:
    print(f"  - {os.path.basename(path)}")

# Load documents
my_documents = load_documents_from_files(file_paths)

# Process for RAG
my_chunks = chunk_documents(my_documents)
chunk_texts = [chunk['text'] for chunk in my_chunks]
my_embeddings = get_embeddings(chunk_texts)
my_vector_store = VectorStore(my_embeddings, my_chunks)

print(f"\n✓ Loaded {len(my_documents)} documents")
print(f"✓ Created {len(my_chunks)} chunks")
print(f"✓ Vector store ready for queries!")
```

### Option 2: Explicit File List

```python
# List your 30 documents explicitly
my_files = [
    "documents/returns_policy.pdf",
    "documents/shipping_info.txt",
    "documents/warranty_coverage.pdf",
    "documents/payment_methods.md",
    "documents/customer_support.txt",
    "documents/account_security.pdf",
    "documents/product_customization.md",
    "documents/bulk_discounts.txt",
    "documents/loyalty_program.pdf",
    "documents/gift_cards.md",
    "documents/privacy_policy.pdf",
    "documents/size_guide.txt",
    "documents/care_instructions.md",
    "documents/order_tracking.pdf",
    "documents/price_match.txt",
    "documents/subscription_service.md",
    "documents/affiliate_program.pdf",
    "documents/environmental_commitment.txt",
    "documents/product_availability.md",
    "documents/technical_support.pdf",
    # ... add remaining 10 documents
]

my_documents = load_documents_from_files(my_files)
```

### Option 3: From URLs (Public Documents)

```python
import requests
from bs4 import BeautifulSoup

def load_from_url(url: str, title: str) -> dict:
    """
    Load document from URL (for publicly available docs)
    """
    response = requests.get(url)
    
    # For HTML pages
    if 'text/html' in response.headers.get('content-type', ''):
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from main content
        content = soup.get_text(separator='\n', strip=True)
    else:
        # For plain text
        content = response.text
    
    return {
        'title': title,
        'content': content,
        'source': url
    }

# Example: Load from public URLs
public_docs = [
    load_from_url('https://example.com/returns', 'Returns Policy'),
    load_from_url('https://example.com/shipping', 'Shipping Info'),
    # ... add more URLs
]

# Process as usual
my_chunks = chunk_documents(public_docs)
```

## Document Quality Tips

### 1. Clean Your Documents

**Remove**:
- Headers and footers
- Page numbers
- Navigation menus (for HTML)
- Boilerplate text
- Irrelevant sections

**Keep**:
- Main content
- Section headings
- Important details
- Contact information

### 2. Structure Matters

**Good Document Structure:**
```markdown
# Returns Policy

## Timeframe
Customers can return items within 30 days...

## Conditions
Items must be in original condition...

## Process
To initiate a return, contact customer support...
```

**Why it helps**:
- Clear headings help with chunking
- Logical sections improve retrieval
- Better context for the LLM

### 3. Consistent Formatting

Use consistent terminology across documents:
- ✅ "Returns" (always)
- ❌ "Returns" in one doc, "Refunds" in another (unless different concepts)

### 4. Avoid Duplicates

If information appears in multiple documents:
- Keep the most detailed version
- Or consolidate into one document
- Duplicates can confuse retrieval

## Example: Pre-processing Documents

```python
def preprocess_document(content: str) -> str:
    """
    Clean document before processing
    """
    # Remove excessive whitespace
    content = ' '.join(content.split())
    
    # Remove page numbers (pattern: "Page 1 of 5")
    import re
    content = re.sub(r'Page \d+ of \d+', '', content)
    
    # Remove email footers
    content = re.sub(r'This email was sent to.*', '', content)
    
    # Remove URLs (optional)
    # content = re.sub(r'http[s]?://\S+', '', content)
    
    return content.strip()

# Use when loading
documents = []
for file_path in file_paths:
    doc = load_single_document(file_path)
    doc['content'] = preprocess_document(doc['content'])
    documents.append(doc)
```

## Special Cases

### Case 1: Very Large Documents

If you have documents > 10,000 words:

```python
# Use smaller chunk size
large_doc_chunks = chunk_documents(
    large_documents,
    chunk_size=300,  # Smaller chunks
    chunk_overlap=30
)
```

### Case 2: Multilingual Documents

For mixed language documents:

```python
# Option 1: Separate by language
english_docs = [doc for doc in documents if doc['language'] == 'en']
spanish_docs = [doc for doc in documents if doc['language'] == 'es']

# Process separately
en_chunks = chunk_documents(english_docs)
es_chunks = chunk_documents(spanish_docs)

# Option 2: Use multilingual embedding model
# Azure OpenAI embeddings support multiple languages
```

### Case 3: Structured Data (Tables, Lists)

For documents with tables:

```python
# Preserve structure in text
structured_content = """
Product Returns Policy

Return Windows:
- Electronics: 14 days
- Clothing: 30 days
- Sale items: Final sale

Refund Processing:
- Standard: 5-7 business days
- Express: 2-3 business days
"""

# The chunker will preserve this structure
```

### Case 4: Scanned PDFs (OCR)

If you have scanned PDFs:

```python
# You'll need OCR (not included in base POC)
# Option 1: Use Azure Computer Vision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

# Option 2: Use pytesseract
import pytesseract
from pdf2image import convert_from_path

def ocr_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
```

## Sample Document Template

Create documents following this template for best results:

```markdown
# [Document Title]

## Overview
Brief summary of what this document covers.

## Key Information

### Section 1
Detailed information about topic 1...

### Section 2
Detailed information about topic 2...

### Section 3
Detailed information about topic 3...

## Important Notes
- Note 1
- Note 2
- Note 3

## Contact
For questions about [topic], contact [details].

---
Last Updated: [Date]
```

## Testing Your Documents

After loading, verify quality:

```python
# Check document loading
print(f"Loaded {len(my_documents)} documents")
for doc in my_documents[:3]:
    print(f"\nTitle: {doc['title']}")
    print(f"Length: {len(doc['content'])} characters")
    print(f"Preview: {doc['content'][:100]}...")

# Check chunking
print(f"\nCreated {len(my_chunks)} chunks")
print(f"Average chunk size: {sum(len(c['text']) for c in my_chunks) / len(my_chunks):.0f} chars")

# Test retrieval
test_query = "What is your return policy?"
test_embedding = get_embeddings([test_query])[0]
results = my_vector_store.search(test_embedding, k=5)

print(f"\nTop result for '{test_query}':")
print(f"  Document: {results[0]['document']['title']}")
print(f"  Similarity: {results[0]['similarity']:.3f}")
print(f"  Preview: {results[0]['document']['text'][:150]}...")
```

## Common Issues and Solutions

### Issue: "No results found"
- **Check**: Are documents loaded correctly?
- **Check**: Is embedding model working?
- **Try**: Use simpler queries first

### Issue: "Wrong documents retrieved"
- **Check**: Document quality (noise, irrelevant text)
- **Try**: Adjust chunk size
- **Try**: Improve document structure

### Issue: "Slow processing"
- **Solution**: Process in batches
- **Solution**: Use smaller chunk size
- **Solution**: Cache embeddings

### Issue: "Out of memory"
- **Solution**: Process documents in batches
- **Solution**: Don't load all documents at once
- **Solution**: Use smaller batch_size in get_embeddings()

## Production Checklist

Before deploying with your actual documents:

- [ ] Documents are cleaned and preprocessed
- [ ] Consistent formatting across documents
- [ ] Removed boilerplate and noise
- [ ] Tested chunking parameters
- [ ] Verified retrieval quality
- [ ] Benchmarked performance
- [ ] Set up document update workflow
- [ ] Implemented backup for vector store
- [ ] Added monitoring for retrieval quality
- [ ] Documented source for each document

## Next Steps

1. Organize your 30 documents in a folder
2. Run the loading code
3. Test with sample queries
4. Adjust chunk parameters if needed
5. Deploy and monitor

For more examples, see `USAGE_EXAMPLES.md`.

