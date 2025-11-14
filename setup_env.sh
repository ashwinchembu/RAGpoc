#!/bin/bash
# Script to create .env file with your Azure credentials

cat > .env << 'ENVFILE'
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://ashwin-demo.openai.azure.com/
AZURE_OPENAI_API_KEY=EVGKsHTL01CyP2WBgxfa9KjPNCrkJpk7js3r60yv5YAedIkOjxsMJQQJ99BIACYeBjFXJ3w3AAABACOGLTVw
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Model Deployment Names (update these to match your actual deployment names)
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_CHAT_DEPLOYMENT=gpt-4
ENVFILE

echo "✓ .env file created successfully!"
echo ""
echo "⚠️  IMPORTANT: You need to update the deployment names!"
echo "   1. Go to https://oai.azure.com/"
echo "   2. Click 'Deployments' to see your model deployment names"
echo "   3. Update AZURE_EMBEDDING_DEPLOYMENT and AZURE_CHAT_DEPLOYMENT in .env"
echo ""
