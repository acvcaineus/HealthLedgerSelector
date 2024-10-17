import requests
from datetime import datetime, timedelta

def fetch_dlt_healthcare_news():
    # NewsAPI endpoint and parameters
    url = "https://newsapi.org/v2/everything"
    
    # Get news from the last 30 days
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    params = {
        'q': '(DLT OR "distributed ledger technology" OR blockchain) AND healthcare',
        'from': thirty_days_ago,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': 'YOUR_API_KEY_HERE'  # Replace with your actual API key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        news_data = response.json()
        
        # Extract relevant information from the API response
        articles = news_data.get('articles', [])
        
        # Process and return the articles
        processed_articles = []
        for article in articles[:5]:  # Limit to 5 articles
            processed_articles.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'publishedAt': article['publishedAt']
            })
        
        return processed_articles
    except requests.RequestException as e:
        print(f"An error occurred while fetching news: {e}")
        return []
