# 🔑 How to Get Azure OpenAI Keys - Visual Guide

## 📍 Where to Find Everything

```
Azure Portal (portal.azure.com)
    │
    ├─► Azure OpenAI Resource
    │       │
    │       ├─► Keys and Endpoint ← YOUR KEYS ARE HERE!
    │       │       • Endpoint URL
    │       │       • Key 1 (Primary)
    │       │       • Key 2 (Secondary)
    │       │
    │       └─► Go to Azure OpenAI Studio
    │               │
    │               └─► Deployments ← DEPLOY MODELS HERE!
    │                       • text-embedding-ada-002
    │                       • gpt-4 (or gpt-35-turbo)
    │
    └─► All done! Copy to .env file
```

---

## 🚀 Quick 3-Step Process

### Step 1️⃣: Get to Azure Portal

**URL**: https://portal.azure.com

**Don't have Azure account?**
- Sign up at https://azure.microsoft.com/free/
- Get $200 free credit
- No credit card required for trial

---

### Step 2️⃣: Create Azure OpenAI Resource

**Option A: Use Portal (Easier)**

1. Click **"Create a resource"**
2. Search: **"Azure OpenAI"**
3. Click **"Create"**

**Configuration:**
```
Subscription: [Your subscription]
Resource Group: Create new → "rag-poc-rg"
Region: East US (recommended)
Name: rag-poc-openai-yourname
Pricing: Standard S0
```

4. Click **"Review + create"**
5. Wait 2-3 minutes ☕

**Option B: Use Azure CLI (Advanced)**
```bash
az login
az group create --name rag-poc-rg --location eastus
az cognitiveservices account create \
  --name rag-poc-openai \
  --resource-group rag-poc-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

---

### Step 3️⃣: Get Your Keys! 🔑

1. Go to your **Azure OpenAI resource** in portal
2. Left menu → Click **"Keys and Endpoint"**
3. **COPY THESE VALUES:**

```
┌─────────────────────────────────────────────────────┐
│ Keys and Endpoint                                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Endpoint:                                          │
│ https://rag-poc-openai-yourname.openai.azure.com/ │
│                                                     │
│ KEY 1                                              │
│ [●●●●●●●●●●●●●●●●●●●●] [Show] [Regenerate]      │
│                                                     │
│ KEY 2                                              │
│ [●●●●●●●●●●●●●●●●●●●●] [Show] [Regenerate]      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Click "Show" to reveal Key 1** ← Copy this entire key!

---

### Step 4️⃣: Deploy Required Models

**Go to Azure OpenAI Studio:**
- From your resource page, click **"Go to Azure OpenAI Studio"**
- Or visit: **https://oai.azure.com/**

#### Deploy Embedding Model

1. Click **"Deployments"** (left menu)
2. Click **"Create new deployment"**
3. Fill in:
   ```
   Select a model: text-embedding-ada-002
   Deployment name: text-embedding-ada-002
   Model version: 2 (default)
   Deployment type: Standard
   Tokens per Minute Rate Limit: 120K
   ```
4. Click **"Create"**
5. Wait ~1 minute ⏱️

#### Deploy Chat Model

1. Click **"Create new deployment"** again
2. Fill in:
   ```
   Select a model: gpt-4 (or gpt-35-turbo for cheaper)
   Deployment name: gpt-4
   Model version: Latest
   Deployment type: Standard
   Tokens per Minute Rate Limit: 10K
   ```
3. Click **"Create"**
4. Wait ~1 minute ⏱️

**Verify**: You should see both deployments listed:
```
✓ text-embedding-ada-002
✓ gpt-4
```

---

### Step 5️⃣: Configure Your .env File

1. **In your terminal:**
   ```bash
   cd /Users/ashwin/zs/RAGpoc
   cp env.template .env
   nano .env   # or use your favorite editor
   ```

2. **Edit .env file with your values:**
   ```env
   # Replace these with YOUR actual values from Azure Portal:
   AZURE_OPENAI_ENDPOINT=https://rag-poc-openai-yourname.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-actual-key-here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   
   # These should match your deployment names exactly:
   AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   AZURE_CHAT_DEPLOYMENT=gpt-4
   ```

3. **Save the file** (Ctrl+O, Enter, Ctrl+X for nano)

---

### Step 6️⃣: Test Your Setup! ✅

```bash
cd /Users/ashwin/zs/RAGpoc
python test_setup.py
```

**Expected output:**
```
✓ AZURE_OPENAI_ENDPOINT: https://...
✓ AZURE_OPENAI_API_KEY: abc123...xyz
✓ Embedding model working!
✓ Chat model working!
🎉 SUCCESS! Your setup is complete!
```

---

## 💡 Important Notes

### Deployment Names Matter!
The **deployment name** (what you named it) is what you use in code, not the model name:
- Use: `text-embedding-ada-002` ← Your deployment name
- Not: `text-embedding-ada-002` ← Model name (in this case they match, but be careful!)

### Keys vs. Deployment Names
```
In Azure Portal → Keys and Endpoint:
  ✓ ENDPOINT: https://your-resource.openai.azure.com/
  ✓ KEY: abc123...

In Azure OpenAI Studio → Deployments:
  ✓ EMBEDDING_DEPLOYMENT: text-embedding-ada-002
  ✓ CHAT_DEPLOYMENT: gpt-4
```

### Region Availability
Not all Azure regions have OpenAI available. Recommended regions:
- ✅ East US
- ✅ South Central US
- ✅ West Europe
- ✅ France Central

---

## 🔧 Troubleshooting

### "I don't see Azure OpenAI in Create Resource"

**Solution**: You need to request access first
1. Go to: https://aka.ms/oai/access
2. Fill out the application form
3. Wait 1-2 business days for approval
4. Check your email for approval notification

### "Deployment failed"

**Possible reasons:**
- Region doesn't support the model → Try different region
- Quota exceeded → Request quota increase in Azure Portal
- Model not available in your subscription → Try different model

### "Authentication failed" when running test

**Check:**
1. ✓ API key is copied correctly (no extra spaces)
2. ✓ Endpoint URL ends with `/`
3. ✓ `.env` file is in the correct directory
4. ✓ Deployment names match exactly (case-sensitive!)

### "Model not found"

**Check:**
1. ✓ Models are deployed in Azure OpenAI Studio
2. ✓ Deployment names match your `.env` file exactly
3. ✓ Wait 1-2 minutes after deployment before testing

---

## 💰 Cost Information

### Free Trial
- New Azure accounts get **$200 credit**
- Valid for 30 days
- No credit card required initially

### Pricing (Pay-as-you-go)
**Embeddings (text-embedding-ada-002):**
- $0.0001 per 1K tokens
- For this POC: ~$0.002 one-time for 43 documents

**GPT-4:**
- Input: $0.03 per 1K tokens
- Output: $0.06 per 1K tokens
- Per query: ~$0.01-0.03

**GPT-3.5-Turbo (cheaper alternative):**
- Input: $0.0005 per 1K tokens
- Output: $0.0015 per 1K tokens
- Per query: ~$0.001-0.003

**Daily cost for 100 queries:**
- With GPT-4: ~$1-3/day
- With GPT-3.5: ~$0.10-0.30/day

---

## ✅ Checklist

Before running the notebook:

- [ ] Azure subscription created
- [ ] Azure OpenAI resource created
- [ ] Keys and endpoint copied
- [ ] Embedding model deployed (`text-embedding-ada-002`)
- [ ] Chat model deployed (`gpt-4` or `gpt-35-turbo`)
- [ ] `.env` file created and configured
- [ ] `test_setup.py` runs successfully
- [ ] Ready to run the notebook! 🚀

---

## 🆘 Need Help?

1. **Check full guide**: Read `SETUP_AZURE.md` for detailed steps
2. **Test your setup**: Run `python test_setup.py`
3. **Azure OpenAI Docs**: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/
4. **Request access**: https://aka.ms/oai/access

---

## 🎉 You're Done!

Once `test_setup.py` passes, you're ready to run:

```bash
jupyter lab azure_rag_poc.ipynb
```

And start querying your 43 real documents! 🚀

