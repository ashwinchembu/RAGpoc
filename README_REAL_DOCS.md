# Real Documents from Public Sources

This POC now uses **43 REAL documents** fetched from public APIs instead of generated sample data!

## 📚 Document Sources

### 1. Wikipedia Articles (18 documents)
Fetched from Wikipedia API covering e-commerce and customer service topics:
- E-commerce
- Customer service
- Online shopping
- Warranty
- Payment systems
- Customer relationship management
- Consumer protection
- Supply chain
- Inventory management
- Retail
- Credit cards
- Refunds
- Privacy policy
- Product returns
- Customer satisfaction
- Payment gateway
- Consumer behavior
- Shopping cart software

### 2. Country Profiles (10 documents)
From REST Countries API with comprehensive country information:
- United States
- United Kingdom
- Germany
- France
- Japan
- Canada
- Australia
- Brazil
- India
- China

Each includes: population, area, languages, currencies, timezones, borders, etc.

### 3. Business Books (15 documents)
From Open Library API covering business topics:
- Business
- Commerce
- Retail
- Marketing
- Customer Service

## 📁 Files Created

### JSON Format
- `fetched_documents.json` - All 43 documents in structured JSON format

### Individual Text Files
- `sample_documents/` - Each document saved as individual .txt file for easy browsing

## 🚀 How to Fetch Fresh Documents

Run the fetch script to get the latest data:

```bash
cd /Users/ashwin/zs/RAGpoc
python fetch_documents.py
```

This will:
1. Fetch articles from Wikipedia
2. Get country data from REST Countries API
3. Fetch book information from Open Library
4. Save everything to `fetched_documents.json`
5. Create individual text files in `sample_documents/`

## 🔧 Customizing Document Sources

Edit `fetch_documents.py` to:
- Change Wikipedia topics (line ~204)
- Select different countries (line ~85)
- Modify book subjects (line ~151)
- Add new public APIs

## 💡 Example Queries to Try

With these real documents, you can ask:

### E-commerce Questions
- "What is e-commerce and how does it work?"
- "What payment methods are commonly used in online shopping?"
- "How does customer relationship management help businesses?"

### Country Information
- "What is the population of Japan?"
- "Which countries border Germany?"
- "What currency does Brazil use?"

### Business Concepts
- "How does supply chain management work?"
- "What is consumer protection?"
- "How are credit cards processed?"

## 🌐 Public APIs Used

### Wikipedia API
- **URL**: https://en.wikipedia.org/w/api.php
- **Authentication**: None required
- **Rate Limit**: Be respectful, add delays
- **Documentation**: https://www.mediawiki.org/wiki/API:Main_page

### REST Countries API
- **URL**: https://restcountries.com/v3.1
- **Authentication**: None required
- **Rate Limit**: None specified
- **Documentation**: https://restcountries.com/

### Open Library API
- **URL**: https://openlibrary.org
- **Authentication**: None required
- **Rate Limit**: None specified
- **Documentation**: https://openlibrary.org/developers/api

## 📊 Document Statistics

```
Total Documents: 43
Total Characters: ~150,000
Average Document Length: ~3,500 characters
Topics Covered: E-commerce, Geography, Business Literature
```

## 🎯 Benefits of Real Documents

1. **Authentic Content**: Real information from reliable sources
2. **Diverse Topics**: Mix of technical, geographical, and business content
3. **Well-Structured**: Professional documentation standards
4. **Always Fresh**: Can re-fetch anytime for updates
5. **Free & Legal**: All from public APIs with no restrictions

## 🔄 Updating Documents

To refresh with latest data:

```bash
python fetch_documents.py
```

The notebook will automatically load the updated `fetched_documents.json`.

## 📝 Adding More Documents

Want more documents? Easy!

1. **Add More Wikipedia Topics**:
   ```python
   wikipedia_topics = [
       'E-commerce',
       'Your_New_Topic_Here',  # Add more
       # ...
   ]
   ```

2. **Add More Countries**:
   ```python
   countries = ['United States', 'Your_Country_Here', ...]
   ```

3. **Add More Book Subjects**:
   ```python
   subjects = ['business', 'your_subject', ...]
   ```

4. **Add New APIs**:
   Create a new function like:
   ```python
   def fetch_from_new_api():
       # Your implementation
       return documents
   ```

## ✅ Verification

Check that documents loaded correctly:

```python
python load_real_documents.py
```

Output should show:
```
✓ Loaded 43 documents from public sources
  - Wikipedia: 18 documents
  - REST Countries API: 10 documents
  - Open Library: 15 documents
```

## 🎉 Ready to Use!

The Jupyter notebook (`azure_rag_poc.ipynb`) is now configured to use these real documents automatically. Just run all cells and start querying!


