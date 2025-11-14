#!/usr/bin/env python3
"""
Fetch 30+ documents from public sources for RAG POC
Uses Wikipedia API and other public sources
"""

import requests
import json
import time
from typing import List, Dict

def fetch_wikipedia_articles(topics: List[str]) -> List[Dict]:
    """
    Fetch articles from Wikipedia API
    """
    documents = []
    base_url = "https://en.wikipedia.org/w/api.php"
    
    print("Fetching documents from Wikipedia...")
    
    headers = {
        'User-Agent': 'RAGPoCBot/1.0 (Educational Purpose)'
    }
    
    for i, topic in enumerate(topics, 1):
        try:
            # Get article content
            params = {
                'action': 'query',
                'format': 'json',
                'titles': topic,
                'prop': 'extracts',
                'explaintext': True,
                'exsectionformat': 'plain',
                'formatversion': 2
            }
            
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'query' in data and 'pages' in data['query']:
                pages = data['query']['pages']
                for page_data in pages:
                    if 'extract' in page_data and len(page_data.get('extract', '')) > 100:
                        # Limit content to first 3000 characters for manageability
                        content = page_data['extract'][:3000]
                        documents.append({
                            'title': page_data['title'],
                            'content': content,
                            'source': f"Wikipedia",
                            'url': f"https://en.wikipedia.org/wiki/{page_data['title'].replace(' ', '_')}"
                        })
                        print(f"  [{i}/{len(topics)}] ✓ Fetched: {page_data['title']}")
                    else:
                        print(f"  [{i}/{len(topics)}] ✗ No content for: {topic}")
            else:
                print(f"  [{i}/{len(topics)}] ✗ No data for: {topic}")
            
            # Rate limiting - be respectful to Wikipedia
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  [{i}/{len(topics)}] ✗ Error fetching {topic}: {e}")
    
    return documents


def fetch_restcountries_data() -> List[Dict]:
    """
    Fetch country information from REST Countries API
    """
    documents = []
    
    print("\nFetching country data from REST Countries API...")
    
    try:
        # Get popular countries
        countries = ['United States', 'United Kingdom', 'Germany', 'France', 'Japan', 
                    'Canada', 'Australia', 'Brazil', 'India', 'China']
        
        for i, country in enumerate(countries, 1):
            try:
                url = f"https://restcountries.com/v3.1/name/{country}"
                response = requests.get(url)
                data = response.json()
                
                if data and len(data) > 0:
                    country_data = data[0]
                    
                    # Create a comprehensive document
                    content = f"""
Country: {country_data.get('name', {}).get('common', country)}

Official Name: {country_data.get('name', {}).get('official', 'N/A')}

Capital: {', '.join(country_data.get('capital', ['N/A']))}

Region: {country_data.get('region', 'N/A')}
Subregion: {country_data.get('subregion', 'N/A')}

Population: {country_data.get('population', 0):,}

Area: {country_data.get('area', 0):,} km²

Languages: {', '.join(country_data.get('languages', {}).values()) if country_data.get('languages') else 'N/A'}

Currencies: {', '.join([f"{v.get('name')} ({v.get('symbol', '')})" for v in country_data.get('currencies', {}).values()]) if country_data.get('currencies') else 'N/A'}

Timezones: {', '.join(country_data.get('timezones', ['N/A']))}

Borders: {', '.join(country_data.get('borders', [])) if country_data.get('borders') else 'No land borders'}

Top Level Domain: {', '.join(country_data.get('tld', ['N/A']))}

Calling Code: +{', +'.join([str(x) for x in country_data.get('idd', {}).get('suffixes', [])]) if country_data.get('idd', {}).get('suffixes') else 'N/A'}

Independent: {'Yes' if country_data.get('independent') else 'No'}

UN Member: {'Yes' if country_data.get('unMember') else 'No'}
                    """.strip()
                    
                    documents.append({
                        'title': f"Country Profile: {country_data.get('name', {}).get('common', country)}",
                        'content': content,
                        'source': 'REST Countries API',
                        'url': 'https://restcountries.com/'
                    })
                    
                    print(f"  [{i}/{len(countries)}] ✓ Fetched: {country}")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  [{i}/{len(countries)}] ✗ Error fetching {country}: {e}")
    
    except Exception as e:
        print(f"  Error accessing REST Countries API: {e}")
    
    return documents


def fetch_open_library_subjects() -> List[Dict]:
    """
    Fetch book information from Open Library API
    """
    documents = []
    
    print("\nFetching book data from Open Library API...")
    
    subjects = ['business', 'commerce', 'retail', 'marketing', 'customer_service']
    
    for subject in subjects:
        try:
            url = f"https://openlibrary.org/subjects/{subject}.json?limit=3"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'works' in data:
                for work in data['works'][:3]:
                    content = f"""
Book: {work.get('title', 'Unknown')}

Authors: {', '.join([author.get('name', 'Unknown') for author in work.get('authors', [])])}

First Published: {work.get('first_publish_year', 'Unknown')}

Subject: {subject.replace('_', ' ').title()}

Description: This book covers topics related to {subject.replace('_', ' ')}. It has been referenced {work.get('edition_count', 0)} times across different editions.

Available editions: {work.get('edition_count', 0)}

Key: {work.get('key', 'N/A')}
                    """.strip()
                    
                    documents.append({
                        'title': f"Book: {work.get('title', 'Unknown')}",
                        'content': content,
                        'source': 'Open Library',
                        'url': f"https://openlibrary.org{work.get('key', '')}"
                    })
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  Error fetching subject {subject}: {e}")
    
    print(f"  ✓ Fetched {len(documents)} book entries")
    return documents


def main():
    """
    Main function to fetch all documents
    """
    print("="*60)
    print("FETCHING DOCUMENTS FROM PUBLIC SOURCES")
    print("="*60)
    
    all_documents = []
    
    # Wikipedia topics - E-commerce and customer service related
    wikipedia_topics = [
        'E-commerce',
        'Customer_service',
        'Online_shopping',
        'Warranty',
        'Payment_system',
        'Shipping',
        'Customer_relationship_management',
        'Consumer_protection',
        'Supply_chain',
        'Inventory',
        'Retail',
        'Credit_card',
        'Refund',
        'Privacy_policy',
        'Product_return',
        'Customer_satisfaction',
        'Electronic_commerce',
        'Payment_gateway',
        'Consumer_behaviour',
        'Shopping_cart_software'
    ]
    
    # Fetch Wikipedia articles
    wiki_docs = fetch_wikipedia_articles(wikipedia_topics)
    all_documents.extend(wiki_docs)
    
    # Fetch country data
    country_docs = fetch_restcountries_data()
    all_documents.extend(country_docs)
    
    # Fetch book data
    book_docs = fetch_open_library_subjects()
    all_documents.extend(book_docs)
    
    # Save to JSON file
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total documents fetched: {len(all_documents)}")
    print(f"  - Wikipedia articles: {len(wiki_docs)}")
    print(f"  - Country profiles: {len(country_docs)}")
    print(f"  - Book entries: {len(book_docs)}")
    
    output_file = 'fetched_documents.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_documents, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Documents saved to: {output_file}")
    
    # Also create individual text files
    import os
    os.makedirs('sample_documents', exist_ok=True)
    
    for i, doc in enumerate(all_documents, 1):
        filename = f"sample_documents/{i:02d}_{doc['title'][:50].replace('/', '_').replace(':', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {doc['title']}\n")
            f.write(f"Source: {doc['source']}\n")
            if 'url' in doc:
                f.write(f"URL: {doc['url']}\n")
            f.write(f"\n{'='*60}\n\n")
            f.write(doc['content'])
    
    print(f"✓ Individual documents saved to: sample_documents/")
    
    print(f"\n{'='*60}")
    print("DONE! You can now use these documents in your RAG system.")
    print(f"{'='*60}\n")
    
    return all_documents


if __name__ == "__main__":
    docs = main()

