import feedparser
from textblob import TextBlob

def get_news(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        summary = entry.summary if 'summary' in entry else entry.title
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'summary': summary
        })
    return articles

def analyze_sentiment(articles):
    for article in articles:
        analysis = TextBlob(article['summary'])
        article['sentiment'] = analysis.sentiment.polarity
    return articles

def fetch_and_analyze_news():
    rbc_feed = 'https://rssexport.rbc.ru/rbcnews/news/20/full.rss'
    investing_feed = 'https://ru.investing.com/rss/market_overview.rss'
    interfax_feed = 'https://www.interfax.ru/rss.asp'
    finam_feed = 'https://www.finam.ru/analytics/rsspoint/'

    rbc_news = get_news(rbc_feed)
    investing_news = get_news(investing_feed)
    interfax_news = get_news(interfax_feed)
    finam_news = get_news(finam_feed)

    analyzed_rbc_news = analyze_sentiment(rbc_news)
    analyzed_investing_news = analyze_sentiment(investing_news)
    analyzed_interfax_news = analyze_sentiment(interfax_news)
    analyzed_finam_news = analyze_sentiment(finam_news)

    return analyzed_rbc_news, analyzed_investing_news, analyzed_interfax_news, analyzed_finam_news
