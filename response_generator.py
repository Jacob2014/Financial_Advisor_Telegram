from stock_data import get_stock_data, analyze_stock_data, get_latest_news


def generate_response(ticker):
    try:
        stock_data = get_stock_data(ticker)
        stock_recommendation = analyze_stock_data(stock_data)
        latest_news_title = get_latest_news(ticker)

        # Создаем ответ с рекомендацией, последней ценой и заголовком последней новости
        response = (
            f"Последние данные по {ticker}:\n"
            f"Открытие: {stock_data['OPEN'].iloc[-1]}\n"
            f"Закрытие: {stock_data['CLOSE'].iloc[-1]}\n"
            f"Максимум: {stock_data['HIGH'].iloc[-1]}\n"
            f"Минимум: {stock_data['LOW'].iloc[-1]}\n"
            f"Объем: {stock_data['VOLUME'].iloc[-1]}\n\n"
            f"Рекомендация на основе графиков: {stock_recommendation}\n"
            f"Последняя новость: {latest_news_title}"
        )
    except Exception as e:
        response = f"Произошла ошибка: {str(e)}"

    return response
