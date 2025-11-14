# 🚀 How to Create Model Deployments in Azure OpenAI

## You Need to Deploy 2 Models

Your Azure OpenAI resource is ready, but you need to **deploy models** before you can use them.

---

## Step-by-Step: Create Deployments

### 1️⃣ Go to Azure OpenAI Studio

**URL**: https://oai.azure.com/

Or from Azure Portal:
- Go to your Azure OpenAI resource
- Click **"Go to Azure OpenAI Studio"** button

---

### 2️⃣ Create Embedding Model Deployment

1. Click **"Deployments"** in the left menu
2. Click **"Create new deployment"** or **"+ Create"** button
3. Fill in the form:

```
┌─────────────────────────────────────────────┐
│ Select a model: text-embedding-ada-002     │
│ Model version: 2 (or Default)              │
│ Deployment name: text-embedding-ada-002    │
│ Deployment type: Standard                   │
│ Tokens per Minute Rate Limit: 120K         │
└─────────────────────────────────────────────┘
```

4. Click **"Create"**
5. Wait ~1 minute for deployment

**Result**: You should see `text-embedding-ada-002` in your deployments list

---

### 3️⃣ Create Chat Model Deployment

1. Click **"Create new deployment"** again
2. Fill in the form:

**Option A: GPT-4 (Better quality, more expensive)**
```
┌─────────────────────────────────────────────┐
│ Select a model: gpt-4                      │
│ Model version: Latest                      │
│ Deployment name: gpt-4                     │
│ Deployment type: Standard                   │
│ Tokens per Minute Rate Limit: 10K          │
└─────────────────────────────────────────────┘
```

**Option B: GPT-3.5-Turbo (Cheaper, still good)**
```
┌─────────────────────────────────────────────┐
│ Select a model: gpt-35-turbo               │
│ Model version: Latest                      │
│ Deployment name: gpt-35-turbo              │
│ Deployment type: Standard                   │
│ Tokens per Minute Rate Limit: 10K          │
└─────────────────────────────────────────────┘
```

3. Click **"Create"**
4. Wait ~1 minute for deployment

---

### 4️⃣ Verify Deployments

In Azure OpenAI Studio → Deployments, you should now see:

```
✓ text-embedding-ada-002  (text-embedding-ada-002)
✓ gpt-4                   (gpt-4)
     OR
✓ gpt-35-turbo            (gpt-35-turbo)
```

---

### 5️⃣ Update Your .env File

Edit your `.env` file to match the deployment names:

**If you deployed gpt-4:**
```bash
nano .env
```

Update to:
```env
AZURE_OPENAI_ENDPOINT=https://ashwin-demo.openai.azure.com/
AZURE_OPENAI_API_KEY=EVGKsHTL01CyP2WBgxfa9KjPNCrkJpk7js3r60yv5YAedIkOjxsMJQQJ99BIACYeBjFXJ3w3AAABACOGLTVw
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_CHAT_DEPLOYMENT=gpt-4
```

**If you deployed gpt-35-turbo:**
```env
AZURE_OPENAI_ENDPOINT=https://ashwin-demo.openai.azure.com/
AZURE_OPENAI_API_KEY=EVGKsHTL01CyP2WBgxfa9KjPNCrkJpk7js3r60yv5YAedIkOjxsMJQQJ99BIACYeBjFXJ3w3AAABACOGLTVw
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_CHAT_DEPLOYMENT=gpt-35-turbo
```

---

### 6️⃣ Test Your Setup

```bash
cd /Users/ashwin/zs/RAGpoc
python test_setup.py
```

You should see:
```
✓ Embedding model working!
✓ Chat model working!
🎉 SUCCESS! Your setup is complete!
```

---

## ❓ Troubleshooting

### "Model not available" or greyed out

**Possible reasons:**
1. **Region doesn't support the model** → Try different region when creating resource
2. **Quota not approved** → Request quota increase in Azure Portal
3. **Model version deprecated** → Select "Latest" version

**Solution:** Try these alternative models:
- For embeddings: `text-embedding-3-small` (newer, cheaper)
- For chat: `gpt-35-turbo` (more widely available)

### Can't find "Create new deployment"

Make sure you're in:
1. **Azure OpenAI Studio** (https://oai.azure.com/)
2. **Deployments** section (left menu)
3. Look for **"+ Create"** or **"Create new deployment"** button at the top

### "Insufficient quota"

1. Go to Azure Portal
2. Navigate to your OpenAI resource
3. Click "Quotas" in left menu
4. Click "Request quota increase"
5. Fill out the form and wait for approval (usually quick)

---

## 💡 Which Models to Choose?

### For This POC (Recommended):

**Embedding Model:**
- `text-embedding-ada-002` ← Most common, well-tested
- OR `text-embedding-3-small` ← Newer, cheaper

**Chat Model:**
- `gpt-35-turbo` ← Good balance of cost/performance
- OR `gpt-4` ← Best quality, more expensive

### Cost Comparison:

**Daily cost for 100 queries:**
- GPT-3.5-Turbo: ~$0.10-0.30/day
- GPT-4: ~$1-3/day

For a POC, **gpt-35-turbo is recommended** to save costs!

---

## 📱 Alternative: Use Azure CLI

If you prefer command line:

```bash
# Deploy embedding model
az cognitiveservices account deployment create \
  --name ashwin-demo \
  --resource-group <your-resource-group> \
  --deployment-name text-embedding-ada-002 \
  --model-name text-embedding-ada-002 \
  --model-version "2" \
  --model-format OpenAI \
  --scale-settings-scale-type "Standard"

# Deploy chat model
az cognitiveservices account deployment create \
  --name ashwin-demo \
  --resource-group <your-resource-group> \
  --deployment-name gpt-35-turbo \
  --model-name gpt-35-turbo \
  --model-version "0301" \
  --model-format OpenAI \
  --scale-settings-scale-type "Standard"
```

---

## ✅ Next Steps

After deployments are created:

1. ✅ Update `.env` with deployment names
2. ✅ Run `python test_setup.py` - should pass!
3. ✅ Run `jupyter lab azure_rag_poc.ipynb`
4. ✅ Start querying your 43 real documents!

---

## 🆘 Still Having Issues?

1. Check Azure OpenAI service status
2. Verify your subscription has OpenAI access
3. Try different region (East US, West Europe)
4. Contact Azure support for quota/access issues

**Need access?** Apply at: https://aka.ms/oai/access

