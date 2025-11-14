#!/usr/bin/env python3
"""
Quick test script to verify Azure OpenAI setup
Run this after configuring your .env file
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are set"""
    print("="*60)
    print("TESTING ENVIRONMENT CONFIGURATION")
    print("="*60)
    
    load_dotenv()
    
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_EMBEDDING_DEPLOYMENT",
        "AZURE_CHAT_DEPLOYMENT"
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("your-"):
            print(f"✗ {var}: NOT SET")
            missing.append(var)
        else:
            # Mask sensitive values
            if "KEY" in var:
                display_value = value[:8] + "..." + value[-4:]
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
    
    if missing:
        print(f"\n❌ Missing variables: {', '.join(missing)}")
        print("   Please configure your .env file")
        return False
    
    print("\n✅ All environment variables configured!\n")
    return True


def test_connection():
    """Test Azure OpenAI connection"""
    print("="*60)
    print("TESTING AZURE OPENAI CONNECTION")
    print("="*60)
    
    try:
        from openai import AzureOpenAI
    except ImportError:
        print("✗ OpenAI library not installed")
        print("  Run: pip install openai")
        return False
    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    print("\n1. Testing Embedding Model...")
    try:
        response = client.embeddings.create(
            input="Hello, world!",
            model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
        )
        embedding_dim = len(response.data[0].embedding)
        print(f"   ✓ Embedding model working!")
        print(f"     Deployment: {os.getenv('AZURE_EMBEDDING_DEPLOYMENT')}")
        print(f"     Dimension: {embedding_dim}")
    except Exception as e:
        print(f"   ✗ Embedding model failed: {e}")
        return False
    
    print("\n2. Testing Chat Model...")
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_CHAT_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello' and nothing else."}
            ],
            max_tokens=10,
            temperature=0
        )
        answer = response.choices[0].message.content
        print(f"   ✓ Chat model working!")
        print(f"     Deployment: {os.getenv('AZURE_CHAT_DEPLOYMENT')}")
        print(f"     Response: {answer}")
    except Exception as e:
        print(f"   ✗ Chat model failed: {e}")
        return False
    
    print("\n✅ All tests passed! Your setup is ready.\n")
    return True


def test_dependencies():
    """Test if required packages are installed"""
    print("="*60)
    print("TESTING DEPENDENCIES")
    print("="*60)
    
    required_packages = {
        "openai": "1.12.0",
        "langchain": "0.1.6",
        "faiss": "1.7.4",
        "tiktoken": "0.5.2",
        "dotenv": "1.0.0",
        "pypdf": "4.0.1",
        "numpy": "1.24.3"
    }
    
    missing = []
    
    for package, expected_version in required_packages.items():
        try:
            if package == "faiss":
                import faiss
                print(f"✓ faiss-cpu: installed")
            elif package == "dotenv":
                from dotenv import load_dotenv
                print(f"✓ python-dotenv: installed")
            elif package == "pypdf":
                import pypdf
                print(f"✓ pypdf: installed")
            else:
                module = __import__(package)
                version = getattr(module, "__version__", "unknown")
                print(f"✓ {package}: {version}")
        except ImportError:
            print(f"✗ {package}: NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AZURE RAG POC - SETUP VERIFICATION")
    print("="*60 + "\n")
    
    # Test dependencies first
    if not test_dependencies():
        print("\n⚠️  Please install missing dependencies and try again.")
        sys.exit(1)
    
    # Test environment configuration
    if not test_environment():
        print("\n⚠️  Please configure your .env file and try again.")
        print("   Copy env.template to .env and fill in your Azure credentials.")
        sys.exit(1)
    
    # Test connection
    if not test_connection():
        print("\n⚠️  Connection test failed. Please check:")
        print("   1. Your Azure OpenAI endpoint URL")
        print("   2. Your API key")
        print("   3. Your model deployment names")
        print("   4. That models are deployed in Azure OpenAI Studio")
        sys.exit(1)
    
    print("="*60)
    print("🎉 SUCCESS! Your setup is complete and working!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Open azure_rag_poc.ipynb in Jupyter")
    print("  2. Run all cells to see the demo")
    print("  3. Replace sample documents with your own")
    print("  4. Start querying your documents!")
    print("\n")


if __name__ == "__main__":
    main()

