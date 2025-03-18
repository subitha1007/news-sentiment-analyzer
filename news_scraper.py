import requests

API_KEY = "5c41f82230c0433aa16229c857b261df"  # Replace with your API key

def get_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch news")
        return []
    
    data = response.json()
    articles = []
    
    for item in data.get("articles", [])[:10]:  # Get top 10 articles
        title = item["title"]
        link = item["url"]
        articles.append({"title": title, "link": link})
    
    return articles

# Example usage
if __name__ == "__main__":
    company = input("Enter company name: ")
    news_articles = get_news(company)
    
    if not news_articles:
        print("No news articles found. Try another company.")
    else:
        for i, article in enumerate(news_articles, 1):
            print(f"{i}. {article['title']} ({article['link']})")
