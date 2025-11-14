# Setting Up Azure OpenAI for RAG POC

This guide walks you through setting up Azure OpenAI Service for the RAG POC.

## Prerequisites

- Azure subscription (free trial available)
- Azure CLI installed (optional but recommended)

## Step-by-Step Setup

### 1. Create Azure OpenAI Resource (5-10 minutes)

#### Option A: Using Azure Portal (Recommended for beginners)

1. **Go to Azure Portal**
   - Navigate to https://portal.azure.com
   - Sign in with your Azure account

2. **Create Resource**
   - Click "Create a resource"
   - Search for "Azure OpenAI"
   - Click "Create"

3. **Configure Resource**
   ```
   Subscription: [Your subscription]
   Resource group: Create new → "rag-poc-rg"
   Region: East US (or closest to you)
   Name: "rag-poc-openai-[yourname]"
   Pricing tier: Standard S0
   ```

4. **Review and Create**
   - Click "Review + create"
   - Wait for deployment (2-3 minutes)
   - Click "Go to resource"

#### Option B: Using Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create \
  --name rag-poc-rg \
  --location eastus

# Create Azure OpenAI resource
az cognitiveservices account create \
  --name rag-poc-openai \
  --resource-group rag-poc-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

### 2. Get Your Credentials (2 minutes)

1. **Navigate to your Azure OpenAI resource**
   - In Azure Portal, go to your resource

2. **Find Keys and Endpoint**
   - Click "Keys and Endpoint" in the left menu
   - You'll see:
     - **Endpoint**: `https://YOUR-RESOURCE.openai.azure.com/`
     - **Key 1**: (click "Show" to reveal)
     - **Key 2**: (backup key)

3. **Copy and Save**
   ```
   Endpoint: https://rag-poc-openai-yourname.openai.azure.com/
   Key: abc123...xyz
   ```

### 3. Deploy Models (5 minutes)

You need to deploy two models: one for embeddings and one for chat.

#### Deploy Embedding Model

1. **Go to Azure OpenAI Studio**
   - From your resource page, click "Go to Azure OpenAI Studio"
   - Or visit https://oai.azure.com/

2. **Navigate to Deployments**
   - Click "Deployments" in the left menu
   - Click "Create new deployment"

3. **Configure Embedding Deployment**
   ```
   Model: text-embedding-ada-002
   Deployment name: text-embedding-ada-002
   Model version: 2 (default)
   Deployment type: Standard
   Tokens per Minute Rate Limit: 120K (adjust as needed)
   ```

4. **Create**
   - Click "Create"
   - Wait for deployment (~1 minute)

#### Deploy Chat Model

1. **Create Another Deployment**
   - Click "Create new deployment" again

2. **Configure Chat Deployment**
   ```
   Model: gpt-4 (or gpt-35-turbo for lower cost)
   Deployment name: gpt-4
   Model version: Latest
   Deployment type: Standard
   Tokens per Minute Rate Limit: 10K (adjust as needed)
   ```

3. **Create**
   - Click "Create"
   - Wait for deployment (~1 minute)

### 4. Verify Deployments

In Azure OpenAI Studio, under "Deployments", you should see:

```
✓ text-embedding-ada-002  (text-embedding-ada-002)
✓ gpt-4                   (gpt-4 / gpt-35-turbo)
```

**Important**: The deployment name (left) is what you'll use in your code, not the model name (right).

### 5. Configure Your POC

1. **Create `.env` file**
   ```bash
   cd /Users/ashwin/zs/RAGpoc
   cp env.template .env
   ```

2. **Edit `.env` with your values**
   ```env
   AZURE_OPENAI_ENDPOINT=https://rag-poc-openai-yourname.openai.azure.com/
   AZURE_OPENAI_API_KEY=abc123...xyz
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   AZURE_CHAT_DEPLOYMENT=gpt-4
   ```

3. **Save the file**

### 6. Test Your Setup (2 minutes)

Run this quick test in Python:

```python
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Test embedding
try:
    response = client.embeddings.create(
        input="Hello, world!",
        model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    )
    print("✓ Embedding model working!")
    print(f"  Dimension: {len(response.data[0].embedding)}")
except Exception as e:
    print(f"✗ Embedding error: {e}")

# Test chat
try:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_CHAT_DEPLOYMENT"),
        messages=[{"role": "user", "content": "Say 'Hello'"}],
        max_tokens=10
    )
    print("✓ Chat model working!")
    print(f"  Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"✗ Chat error: {e}")
```

If both tests pass, you're ready to run the RAG POC! 🎉

## Cost Estimation

### Pay-as-you-go Pricing (as of 2024)

#### Embedding Model (text-embedding-ada-002)
- **Cost**: $0.0001 per 1K tokens
- **For this POC**: 
  - 30 documents × ~500 tokens each = 15K tokens
  - Embedding cost: ~$0.0015 (one-time)
  - Query embedding: ~$0.0001 per query

#### Chat Model

**GPT-4**
- **Input**: $0.03 per 1K tokens
- **Output**: $0.06 per 1K tokens
- **Per query**: ~$0.01-0.03 (depends on context)

**GPT-3.5-Turbo** (cheaper alternative)
- **Input**: $0.0005 per 1K tokens
- **Output**: $0.0015 per 1K tokens
- **Per query**: ~$0.001-0.003

### Example: 30 Documents, 100 Queries/day

**Setup (one-time)**:
- Embedding 30 docs: $0.002

**Daily Usage**:
- Query embeddings: $0.01
- GPT-4 answers: $1.50-3.00
- GPT-3.5 answers: $0.10-0.30

**Monthly (GPT-4)**: ~$50-100
**Monthly (GPT-3.5)**: ~$5-10

### Cost Optimization Tips

1. **Use GPT-3.5-Turbo for testing**
   - 10x cheaper than GPT-4
   - Good enough for most use cases

2. **Cache frequent queries**
   - Store common Q&A pairs
   - Reduce API calls by 50-80%

3. **Optimize chunk size**
   - Smaller chunks = less context = lower cost
   - Find balance between quality and cost

4. **Set rate limits**
   - Prevent unexpected costs
   - Configure in Azure Portal

5. **Monitor usage**
   - Check Azure Cost Management
   - Set budget alerts

## Troubleshooting

### "Resource not found"
- **Check**: Endpoint URL is correct
- **Check**: Resource is fully deployed
- **Wait**: Sometimes takes 5-10 minutes after creation

### "Authentication failed"
- **Check**: API key is copied correctly (no extra spaces)
- **Check**: Using Key 1 or Key 2 from "Keys and Endpoint"
- **Try**: Regenerate keys in Azure Portal

### "Model not found"
- **Check**: Deployment name matches exactly (case-sensitive)
- **Check**: Model is deployed in Azure OpenAI Studio
- **Wait**: Deployment can take 1-2 minutes

### "Rate limit exceeded"
- **Check**: Your token rate limit in deployments
- **Increase**: Request higher quota in Azure Portal
- **Wait**: Rate limits reset after 1 minute

### "Quota exceeded"
- **Check**: Your subscription limits
- **Request**: Quota increase via Azure Portal
  - Go to resource → Quotas → Request increase

### "Access denied" or "Subscription not enabled"
- **Apply**: Azure OpenAI access (can take 1-2 business days)
- **Visit**: https://aka.ms/oai/access
- **Alternative**: Use OpenAI API directly (not Azure) for testing

## Security Best Practices

1. **Never commit `.env` to git**
   ```bash
   # Already in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use separate keys for dev/prod**
   - Create separate resources
   - Rotate keys periodically

3. **Enable Azure RBAC**
   - Use managed identities in production
   - Avoid API keys if possible

4. **Monitor usage**
   - Set up Azure Monitor alerts
   - Review access logs regularly

5. **Set spending limits**
   - Configure budget alerts
   - Set per-minute rate limits

## Next Steps

✅ Azure OpenAI resource created  
✅ Models deployed  
✅ Credentials configured  
✅ Connection tested  

Now you're ready to:
1. Run the Jupyter notebook: `jupyter lab azure_rag_poc.ipynb`
2. Follow the QUICKSTART.md guide
3. Load your 30 documents
4. Start querying!

## Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Quota Management](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quotas-limits)
- [Best Practices](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/best-practices)

## Support

- Azure OpenAI Support: https://azure.microsoft.com/support/
- Community Forum: https://techcommunity.microsoft.com/
- Stack Overflow: Tag `azure-openai`

