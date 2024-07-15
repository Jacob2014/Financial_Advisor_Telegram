import schedule
import time
import threading
from news_fetcher import fetch_and_analyze_news

def schedule_news_fetching():
    schedule.every(10).minutes.do(fetch_and_analyze_news)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    threading.Thread(target=schedule_news_fetching).start()
