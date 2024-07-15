import requests
import pandas as pd
import talib
from datetime import datetime, timedelta

NEWS_API_KEY = '2af9e6029bb44ec19b0c7abc1bf4ae9f'

TICKER_COMPANY_MAPPING = {
    'SBER': 'Сбербанк',
    'GAZP': 'Газпром',
    'LKOH': 'Лукойл',
    # Добавьте другие тикеры и компании по мере необходимости
}


def get_moex_data(security_ticker, start_date, end_date):
    base_url = "https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/"
    url = f"{base_url}{security_ticker}.json"
    params = {
        'from': start_date,
        'till': end_date,
        'iss.meta': 'off',
        'iss.only': 'history',
        'history.columns': 'TRADEDATE,OPEN,CLOSE,HIGH,LOW,VOLUME'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['history']['data']
    else:
        response.raise_for_status()


def get_stock_data(ticker):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')  # последние 30 дней

    data = get_moex_data(ticker, start_date, end_date)
    df = pd.DataFrame(data, columns=['TRADEDATE', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME'])
    df['TRADEDATE'] = pd.to_datetime(df['TRADEDATE'])
    df.set_index('TRADEDATE', inplace=True)

    df['RSI'] = talib.RSI(df['CLOSE'], timeperiod=14)

    return df


def analyze_stock_data(df):
    last_rsi = df['RSI'].iloc[-1]

    if last_rsi < 30:
        recommendation = "Покупать"
    elif last_rsi > 70:
        recommendation = "Продавать"
    else:
        recommendation = "Держать"

    return recommendation


def get_latest_news(ticker):
    company_name = TICKER_COMPANY_MAPPING.get(ticker, ticker)
    query = f"{company_name}"
    url = f"https://newsapi.org/v2/everything?q={query}&language=ru&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles')
        if articles:
            latest_news = articles[0]['title']
        else:
            latest_news = "Нет новостей по этому тикеру."
    else:
        latest_news = "Не удалось получить новости."

    return latest_news
